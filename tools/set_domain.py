#!/usr/bin/env python3
"""
Cambia el dominio del sitio en TODOS lados de una sola vez.

Mientras el nombre/dominio no esté decidido, el sitio usa el placeholder
`https://tu-dominio.com` en canonical, og:url, JSON-LD (@id), sitemap, robots,
llms.txt y en la constante DOMAIN de los generadores. Este script reemplaza ese
placeholder por el dominio real en todos los archivos de texto del repo, para que
no haya que buscarlo a mano archivo por archivo.

Uso:
    python3 tools/set_domain.py https://midominio.com
    python3 tools/set_domain.py https://midominio.com --dry-run   # solo muestra

Después de correrlo, regenera lo generado para que quede consistente:
    python3 tools/build_pages.py && python3 tools/build_about.py

Nota: usa siempre el ORIGEN sin diagonal final (https://midominio.com), sin ruta.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = "https://tu-dominio.com"

# No tocar binarios, dependencias ni el build de Pages (se regenera aparte).
BLOCKED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__",
                ".pytest_cache", "docs", "og", "img", "assets"}
TEXT_SUFFIXES = {".html", ".css", ".js", ".json", ".webmanifest", ".xml",
                 ".txt", ".py", ".md"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("domain", help="Dominio real, p.ej. https://midominio.com (solo origen)")
    ap.add_argument("--dry-run", action="store_true", help="No escribe; solo reporta")
    args = ap.parse_args()

    new = args.domain.rstrip("/")
    if not new.startswith("http"):
        sys.exit("El dominio debe incluir el esquema, p.ej. https://midominio.com")
    if new == PLACEHOLDER:
        sys.exit("Ese es el placeholder. Pasa el dominio real.")

    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        rel = path.relative_to(ROOT)
        if any(part in BLOCKED_DIRS for part in rel.parts):
            continue
        if path.name == "set_domain.py":
            continue
        text = path.read_text(encoding="utf-8")
        n = text.count(PLACEHOLDER)
        if not n:
            continue
        print(f"  {rel}: {n} ocurrencia(s)")
        changed += n
        if not args.dry_run:
            path.write_text(text.replace(PLACEHOLDER, new), encoding="utf-8")

    verb = "se cambiarían" if args.dry_run else "cambiadas"
    print(f"\n{changed} ocurrencia(s) {verb}  ->  {new}")
    if not args.dry_run and changed:
        print("Ahora regenera:  python3 tools/build_pages.py && python3 tools/build_about.py")


if __name__ == "__main__":
    main()
