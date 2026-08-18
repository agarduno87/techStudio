#!/usr/bin/env python3
"""
Procesa los retratos del equipo para la página About.

Uso:
    python3 tools/build_portraits.py ruta/antonio.jpg ruta/samuel.png

O sin argumentos, si los originales ya están en assets/portraits/:
    python3 tools/build_portraits.py

Salida (en img/):
    antonio-garduno-640.jpg / .webp     retina
    antonio-garduno-320.jpg / .webp     tamaño de presentación
    samuel-gonzalez-640.jpg / .webp
    samuel-gonzalez-320.jpg / .webp

Dos decisiones de diseño que el script aplica:

1. Ambos retratos salen en ESCALA DE GRISES. Los originales vienen distintos —
   uno en blanco y negro sobre fondo oscuro, otro a color sobre pared gris — y
   puestos lado a lado se ven como dos personas de dos sitios distintos. En
   monocromo se leen como un equipo, y encaja con la sobriedad del resto.

2. Cada retrato lleva su propio encuadre. Los originales están tomados a
   distancias distintas —uno es primer plano, el otro cuerpo entero— y sin
   ajustar, uno de los dos se ve lejano y el otro encima. El recorte los deja
   con la cabeza al mismo tamaño relativo, que es lo que hace que se lean como
   una pareja de retratos y no como dos fotos sueltas.

Se generan WebP y JPEG: el navegador toma el WebP (pesa la mitad) y el JPEG
queda de respaldo. Los dos anchos evitan servir 640 px a una tarjeta de 320.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "img"
WIDTHS = (640, 320)

# (slug, centro X, centro Y, lado del recorte) — todo como proporción del original
PEOPLE = [
    ("antonio-garduno", 0.50, 0.50, 1.00),   # ya viene en primer plano
    ("samuel-gonzalez", 0.55, 0.27, 0.52),   # cuerpo entero: se acerca a la cara
]


def process(src: Path, slug: str, cx: float, cy: float, side_ratio: float) -> None:
    from PIL import Image, ImageOps

    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        fondo = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        fondo.paste(im, mask=im.split()[-1])
        im = fondo
    else:
        im = im.convert("RGB")

    # Recorte cuadrado alrededor del punto de interés, sin salirse del original
    w, h = im.size
    side = int(min(w, h) * side_ratio)
    left = int(max(0, min(w - side, cx * w - side / 2)))
    top = int(max(0, min(h - side, cy * h - side / 2)))
    im = im.crop((left, top, left + side, top + side))

    # Monocromo, con un ajuste suave de contraste para que ambos casen
    im = ImageOps.grayscale(im)
    im = ImageOps.autocontrast(im, cutoff=(0.5, 0.5))
    im = im.convert("RGB")

    OUT.mkdir(exist_ok=True)
    for width in WIDTHS:
        resized = im.resize((width, width), Image.LANCZOS)
        resized.save(OUT / f"{slug}-{width}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
        resized.save(OUT / f"{slug}-{width}.webp", "WEBP", quality=80, method=6)
        print(f"  img/{slug}-{width}.jpg  +  .webp")


def main() -> None:
    args = sys.argv[1:]
    if args:
        sources = [Path(a) for a in args]
    else:
        assets = ROOT / "assets" / "portraits"
        sources = sorted(assets.glob("*")) if assets.exists() else []

    if len(sources) != len(PEOPLE):
        print("Uso: python3 tools/build_portraits.py <foto-antonio> <foto-samuel>")
        print("O deja los dos originales en assets/portraits/ y corre sin argumentos.")
        sys.exit(1)

    for src, (slug, cx, cy, side_ratio) in zip(sources, PEOPLE):
        if not src.exists():
            print(f"No encontré {src}")
            sys.exit(1)
        process(src, slug, cx, cy, side_ratio)

    print("\nRetratos listos.")


if __name__ == "__main__":
    main()
