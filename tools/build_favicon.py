#!/usr/bin/env python3
"""
Genera los iconos del sitio a partir de la marca: monograma TS en dorado sobre
navy, el mismo cuadro que aparece en la cabecera.

Uso:
    python3 tools/build_favicon.py

Salida (en la raíz del proyecto):
    favicon.svg          moderno, vectorial, nítido a cualquier tamaño
    favicon.ico          respaldo 16/32/48 px para navegadores viejos y crawlers
    apple-touch-icon.png 180×180, para "Añadir a inicio" en iOS
    icon-192.png         Android / PWA
    icon-512.png         Android / PWA
    site.webmanifest     metadatos de instalación

Para cambiar la marca, edita las constantes de aquí abajo y vuelve a ejecutar.
Requiere Pillow solo para los PNG/ICO:  pip install Pillow
El SVG se escribe a mano y no depende de nada.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NAVY = (14, 36, 57)        # --ink   #0E2439
GOLD = (201, 162, 39)      # --gold-soft #C9A227
PAPER = (244, 246, 248)    # --paper-2  #F4F6F8
LETTERS = "TS"

SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Technical Transformation Studio">
  <title>Technical Transformation Studio</title>
  <rect width="64" height="64" rx="8" fill="#0E2439"/>
  <rect x="5" y="5" width="54" height="54" rx="5" fill="none" stroke="#C9A227" stroke-width="2"/>
  <text x="32" y="44"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="32" font-weight="400" letter-spacing="0.5"
        text-anchor="middle" fill="#F4F6F8">{LETTERS}</text>
</svg>
"""

MANIFEST = """{
  "name": "Technical Transformation Studio",
  "short_name": "TTS",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#0E2439",
  "background_color": "#E9ECEF",
  "display": "browser"
}
"""


def draw(size: int, radius_ratio: float = 0.125):
    """Dibuja el icono a `size` px. Se renderiza al cuádruple y se reduce:
    a 16 px el antialiasing es la diferencia entre una marca legible y una mancha."""
    from PIL import Image, ImageDraw, ImageFont

    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # A 16 px cada píxel cuenta: se reduce el redondeo para no comerse el área útil.
    radius = int(s * (radius_ratio if size >= 32 else 0.07))
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=radius, fill=NAVY)

    # Filete dorado: se omite por debajo de 32 px porque a ese tamaño
    # se convierte en ruido y come el espacio de las letras.
    if size >= 32:
        inset = max(2, int(s * 0.08))
        d.rounded_rectangle(
            [inset, inset, s - 1 - inset, s - 1 - inset],
            radius=max(2, radius - inset // 2),
            outline=GOLD,
            width=max(2, int(s * 0.031)),
        )

    font = None
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/Library/Fonts/Georgia Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ):
        if Path(candidate).exists():
            # Las letras van más grandes en los tamaños chicos: al reducir, el
            # antialiasing adelgaza el trazo y un serif fino se vuelve gris.
            font = ImageFont.truetype(candidate, int(s * (0.46 if size >= 32 else 0.60)))
            break
    if font is None:
        font = ImageFont.load_default()

    box = d.textbbox((0, 0), LETTERS, font=font)
    d.text(
        ((s - (box[2] - box[0])) / 2 - box[0], (s - (box[3] - box[1])) / 2 - box[1]),
        LETTERS,
        font=font,
        fill=PAPER if size >= 32 else (255, 255, 255),
    )

    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    (ROOT / "favicon.svg").write_text(SVG, encoding="utf-8")
    (ROOT / "site.webmanifest").write_text(MANIFEST, encoding="utf-8")
    print("  favicon.svg")
    print("  site.webmanifest")

    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("\n  Pillow no está instalado: se omitieron los PNG/ICO.")
        print("  Instálalo con:  pip install Pillow   y vuelve a correr esto.")
        sys.exit(0)

    # El ICO se arma de mayor a menor: Pillow toma la primera imagen como base,
    # y si es la chica escala hacia arriba y las grandes salen borrosas.
    # Cada tamaño se dibuja por separado para que el filete dorado se decida
    # por resolución y no por un reescalado.
    ico_sizes = [48, 32, 16]
    frames = [draw(n) for n in ico_sizes]
    frames[0].save(ROOT / "favicon.ico", format="ICO",
                   sizes=[(n, n) for n in ico_sizes], append_images=frames[1:])
    print("  favicon.ico (48, 32, 16)")

    for name, size in (("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
        draw(size).save(ROOT / name, format="PNG")
        print(f"  {name}")

    print("\nIconos generados.")


if __name__ == "__main__":
    main()
