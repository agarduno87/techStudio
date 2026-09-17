#!/usr/bin/env python3
"""
Construye el PREVIEW "datarahub" (re-skin oscuro) del sitio COMPLETO en
docs/datarahub/, sin tocar producción (docs/ en la raíz).

Qué hace:
  1. Empaqueta el sitio entero con build_github_pages.py, base /techStudio/datarahub,
     salida docs/datarahub/  (mismas páginas, secciones y funcionalidades).
  2. Reemplaza styles.css por el sistema oscuro (styles-datarahub.css).
  3. Recolorea el cometa del masthead a esmeralda (solo dentro del <svg class="brandmark">),
     y ajusta el theme-color a fondo oscuro.

Uso:
    python3 tools/build_preview_datarahub.py

Queda vivo (una vez publicado /docs) en:
    https://<usuario>.github.io/techStudio/datarahub/
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "datarahub"
BASE = "/techStudio/datarahub"
MAILTO = "ing.antoniogz@gmail.com"

# Cometa: navy/dorado (paper) -> esmeralda/azul (dark). Solo dentro del brandmark.
COMET_SWAP = {
    "#16324C": "#3B82F6",   # cola del gradiente -> azul
    "#C9A227": "#10B981",   # cabeza + glow -> esmeralda (aparece 3 veces)
    "#0E2439": "#F4F6F8",   # punto central -> claro (fondo oscuro)
}
_BRANDMARK = re.compile(r'<svg class="brandmark".*?</svg>', re.S)


def recolor_comet(html: str) -> str:
    def _swap(m):
        block = m.group(0)
        for a, b in COMET_SWAP.items():
            block = block.replace(a, b)
        return block
    return _BRANDMARK.sub(_swap, html)


def main() -> None:
    # 1. Empaquetar el sitio completo hacia docs/datarahub/
    cmd = [sys.executable, str(ROOT / "tools" / "build_github_pages.py"),
           "--base", BASE, "--out", "docs/datarahub", "--mailto", MAILTO]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("build_github_pages falló:\n" + r.stdout + r.stderr)

    # 2. Piel oscura
    dark = (ROOT / "styles-datarahub.css").read_text(encoding="utf-8")
    (OUT / "styles.css").write_text(dark, encoding="utf-8")

    # 3. Recolorear el cometa + theme-color oscuro, en cada HTML del preview
    n = 0
    for page in OUT.rglob("*.html"):
        t = page.read_text(encoding="utf-8")
        new = recolor_comet(t).replace('content="#0E2439"', 'content="#08131A"')
        if new != t:
            page.write_text(new, encoding="utf-8")
            n += 1

    print(f"  preview datarahub -> {OUT.relative_to(ROOT)}")
    print(f"  styles.css oscuro + cometa esmeralda en {n} páginas")
    print(f"  vivo en: https://agarduno87.github.io{BASE}/  (tras publicar /docs)")


if __name__ == "__main__":
    main()
