#!/usr/bin/env python3
"""
Genera las imágenes Open Graph: la tarjeta que se ve cuando alguien comparte una
liga del sitio por WhatsApp, LinkedIn, Slack o Twitter.

Uso:
    python3 tools/build_og.py

Salida:
    og/<slug>.png   1200×630, una por página

Sin estas imágenes, compartir cualquier liga muestra una tarjeta gris con texto
chico. Con ellas, muestra el título de la página sobre la marca del estudio.
Cuesta un archivo por página y cambia por completo cómo se ve tu sitio cuando
alguien lo reenvía — que es exactamente el momento en que un prospecto decide si
te abre o no.

Los títulos se leen de los generadores, así que una página nueva hereda su
tarjeta sin tocar este archivo.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

W, H = 1200, 630
NAVY = (14, 36, 57)
GOLD = (201, 162, 39)
PAPER = (244, 246, 248)
MUTED = (169, 186, 203)

FONT_SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
]
FONT_MONO = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/System/Library/Fonts/Menlo.ttc",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
]


def font(paths, size):
    from PIL import ImageFont
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def wrap(draw, text, f, max_width):
    words, lines, line = text.split(), [], ""
    for w in words:
        probe = f"{line} {w}".strip()
        if draw.textlength(probe, font=f) <= max_width:
            line = probe
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def card(slug: str, kicker: str, title: str) -> None:
    from PIL import Image, ImageDraw

    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    pad = 80
    d.rectangle([pad, pad, W - pad, H - pad], outline=GOLD, width=2)

    # Monograma
    mono_box = [pad + 44, pad + 44, pad + 44 + 72, pad + 44 + 72]
    d.rectangle(mono_box, outline=PAPER, width=2)
    f_mark = font(FONT_SERIF, 34)
    b = d.textbbox((0, 0), "TS", font=f_mark)
    d.text((mono_box[0] + (72 - (b[2] - b[0])) / 2 - b[0],
            mono_box[1] + (72 - (b[3] - b[1])) / 2 - b[1]), "TS", font=f_mark, fill=PAPER)

    f_kick = font(FONT_MONO, 20)
    d.text((pad + 140, pad + 62), kicker.upper()[:46], font=f_kick, fill=GOLD)

    # Título: se ajusta el cuerpo hasta que quepa en cuatro líneas
    max_w = W - 2 * pad - 88
    for size in (66, 58, 50, 44, 38):
        f_title = font(FONT_SERIF, size)
        lines = wrap(d, title, f_title, max_w)
        if len(lines) <= 4:
            break
    lh = int(size * 1.22)
    y = pad + 190
    for line in lines[:4]:
        d.text((pad + 44, y), line, font=f_title, fill=PAPER)
        y += lh

    f_foot = font(FONT_MONO, 20)
    d.text((pad + 44, H - pad - 56), "TECHNICAL TRANSFORMATION STUDIO · QUERÉTARO, MX",
           font=f_foot, fill=MUTED)

    out = ROOT / "og"
    out.mkdir(exist_ok=True)
    img.save(out / f"{slug}.png", "PNG", optimize=True)
    print(f"  og/{slug}.png")


def main() -> None:
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("Falta Pillow.  pip install Pillow")
        sys.exit(1)

    cards = [
        ("home", "Five practices",
         "Technical work, delivered under a written scope."),
        ("about", "Who does the work",
         "Two people, and both of them senior."),
        ("work", "Evidence",
         "Systems that exist, with the numbers attached."),
        ("privacy", "Legal", "Privacy notice"),
        ("terms", "Legal", "Terms of use"),
    ]

    import build_pages
    for p in build_pages.PAGES:
        cards.append((p["slug"], "Practice " + p["num"], p["h1_en"]))

    import build_cases
    for c in build_cases.CASES:
        kicker = c["kicker_en"].replace("&amp;", "&").split("·")[0].strip()
        cards.append((f"case-{c['slug']}", kicker, c["h1_en"]))

    for slug, kicker, title in cards:
        card(slug, kicker, title)

    print(f"\n{len(cards)} tarjetas generadas.")


if __name__ == "__main__":
    main()
