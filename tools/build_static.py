#!/usr/bin/env python3
"""
Empaqueta SOLO los archivos estaticos del sitio en dist/ y genera un zip listo
para subir al hosting compartido (cPanel/Neubox) y extraer dentro de public_html/.

    python3 tools/build_static.py
    python3 tools/build_static.py --out dist --zip neubox-static.zip
    python3 tools/build_static.py --no-zip

DIFERENCIA CON build_github_pages.py
------------------------------------
Aquel empaqueta en docs/ para GitHub Pages, reescribe las rutas absolutas a un
subdirectorio (/mi-repo/...) e inyecta un formulario por mailto. Este NO reescribe
nada: el sitio vive en la RAIZ del dominio, asi que /work/ y /styles.css ya son
correctos. Tampoco inyecta nada: sube el sitio tal cual, sin backend.

POR QUE ES WHITELIST Y NO BLACKLIST
-----------------------------------
Los archivos permitidos se listan uno por uno. Todo lo que no este aqui queda
fuera por definicion, asi que api/ (codigo y .env), tools/, tests/, docs/,
assets/ y .git no pueden colarse ni por descuido.

Multiplataforma: solo la biblioteca estandar de Python (Linux, macOS, Windows).
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "dist"
DEFAULT_ZIP = ROOT / "neubox-static.zip"

# Archivos sueltos en la raiz que SI se publican.
WHITELIST_FILES = [
    "index.html",
    "styles.css",
    "app.js",
    "i18n.js",
    "favicon.ico",
    "favicon.svg",
    "apple-touch-icon.png",
    "icon-192.png",
    "icon-512.png",
    "site.webmanifest",
    "robots.txt",
    "sitemap.xml",
]

# Carpetas que SI se publican, completas.
WHITELIST_DIRS = [
    "i18n",
    "services",
    "work",
    "about",
    "legal",
    "img",
    "og",
]

# Nunca se publica un archivo con estas extensiones, pase lo que pase.
BLOCKED_SUFFIX = {
    ".py", ".sh", ".db", ".sqlite3", ".pyc", ".env",
    ".md", ".log", ".ini", ".bak", ".zip",
}

# Excepciones dentro de carpetas permitidas: la plantilla no se carga nunca.
EXCLUDE_NAMES = {"_template.js"}


def die(message: str) -> None:
    print(f"XX {message}", file=sys.stderr)
    raise SystemExit(1)


def collect_sources() -> list[tuple[Path, Path]]:
    """Devuelve pares (origen_absoluto, ruta_relativa). Falla si falta algo."""
    found: list[tuple[Path, Path]] = []

    for name in WHITELIST_FILES:
        src = ROOT / name
        if not src.is_file():
            die(f"falta el archivo esperado: {name}")
        found.append((src, Path(name)))

    for dirname in WHITELIST_DIRS:
        base = ROOT / dirname
        if not base.is_dir():
            die(f"falta la carpeta esperada: {dirname}/")
        for src in sorted(base.rglob("*")):
            if not src.is_file():
                continue
            rel = src.relative_to(ROOT)
            if src.name in EXCLUDE_NAMES or src.name.startswith("."):
                continue
            if src.suffix.lower() in BLOCKED_SUFFIX:
                continue
            found.append((src, rel))

    return found


def build(out: Path, sources: list[tuple[Path, Path]]) -> int:
    if out == ROOT:
        die("la salida no puede ser la raiz del proyecto")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)

    for src, rel in sources:
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    return len(sources)


def audit(out: Path) -> None:
    """Cinturon de seguridad: si algo prohibido llego a la salida, se aborta."""
    offenders = [
        p.relative_to(out).as_posix()
        for p in out.rglob("*")
        if p.is_file() and p.suffix.lower() in BLOCKED_SUFFIX
    ]
    if offenders:
        die("archivos que no deberian publicarse: " + ", ".join(sorted(offenders)))


def make_zip(zip_path: Path, out: Path) -> int:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    files = [p for p in sorted(out.rglob("*")) if p.is_file()]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            # arcname sin carpeta contenedora: al extraer dentro de public_html/
            # la estructura queda correcta directamente.
            zf.write(path, path.relative_to(out).as_posix())
    return len(files)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Empaqueta el sitio estatico en dist/ para subirlo a cPanel."
    )
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help="carpeta de salida (por defecto: dist/)")
    ap.add_argument("--zip", dest="zip_path", default=str(DEFAULT_ZIP),
                    help="ruta del zip (por defecto: neubox-static.zip)")
    ap.add_argument("--no-zip", action="store_true",
                    help="no generar el zip, solo la carpeta")
    args = ap.parse_args()

    out = Path(args.out).expanduser().resolve()

    sources = collect_sources()
    total = build(out, sources)
    audit(out)

    print(f"  {out}")
    print(f"  {total} archivos copiados")

    if not args.no_zip:
        zip_path = Path(args.zip_path).expanduser().resolve()
        make_zip(zip_path, out)
        print(f"  {zip_path}")

    print("\n  Sube el CONTENIDO de esa carpeta a public_html/ (raiz del dominio),")
    print("  o sube el zip y extraelo dentro de public_html/.")


if __name__ == "__main__":
    main()
