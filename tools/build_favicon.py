#!/usr/bin/env python3
"""
Genera los iconos del sitio a partir de la marca: el logo COMETA en dorado sobre
navy, el mismo mark que aparece en la cabecera.

Uso:
    python3 tools/build_favicon.py

Salida (en la raíz del proyecto):
    favicon.svg          moderno, vectorial, nítido a cualquier tamaño
    favicon.ico          respaldo 16/32/48 px para navegadores viejos y crawlers
    apple-touch-icon.png 180×180, para "Añadir a inicio" en iOS
    icon-192.png         Android / PWA
    icon-512.png         Android / PWA
    site.webmanifest     metadatos de instalación

El SVG se escribe a mano; los PNG/ICO se dibujan con Pillow (tools/comet.py).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))  # para importar comet.py

# El SVG es la fuente moderna: cometa dorado sobre caja navy redondeada.
# feGaussianBlur da el glow de la cabeza; el gradiente va del navy (cola, se funde
# con el fondo) al dorado. Sin style= inline: la CSP del sitio queda contenta.
SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" role="img" aria-label="Datara Hub">
  <title>Datara Hub</title>
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#16324C" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#C9A227" stop-opacity="1"/>
    </linearGradient>
    <filter id="f" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.5"/></filter>
  </defs>
  <rect x="2" y="2" width="116" height="116" rx="19" fill="#F4F6F8" stroke="#C9A227" stroke-width="3"/>
  <circle cx="20.53" cy="45.64" r="14" fill="#C9A227" opacity="0.22" filter="url(#f)"/>
  <path d="M 60,18 A 42,42 0 1 1 20.53,45.64" fill="none" stroke="url(#g)" stroke-width="6.5" stroke-linecap="round"/>
  <circle cx="60" cy="60" r="3.4" fill="#0E2439" opacity="0.9"/>
  <circle cx="20.53" cy="45.64" r="7" fill="#C9A227"/>
</svg>
"""

MANIFEST = """{
  "name": "Datara Hub",
  "short_name": "Datara Hub",
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
    """Dibuja el icono a `size` px. Se renderiza al cuádruple y se reduce, para que
    el antialiasing conserve el trazo del cometa a 16 px."""
    from PIL import Image, ImageDraw
    from comet import draw_comet, NAVY, GOLD, PAPER

    scale = 4
    s = size * scale
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    radius = int(s * (radius_ratio if size >= 32 else 0.07))
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=radius, fill=PAPER + (255,))
    # Filete dorado (se omite <32 px: a ese tamaño es ruido).
    if size >= 32:
        bw = max(2, int(s * 0.028))
        d.rounded_rectangle([bw, bw, s - 1 - bw, s - 1 - bw],
                            radius=max(2, radius - bw), outline=GOLD + (255,), width=bw)

    # Cometa centrado, punto navy (visible sobre paper). A tamaños chicos, trazo más grueso.
    cx = cy = s / 2
    r = s * 0.33
    width_ratio = 0.12 if size >= 32 else 0.17
    draw_comet(img, cx, cy, r, dot=NAVY, width_ratio=width_ratio)

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
