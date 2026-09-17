#!/usr/bin/env python3
"""
Dibuja el logo "cometa" de Datara Hub con Pillow, para el favicon y las tarjetas OG
(que son PNG, no SVG). Reproduce el mismo trazo del SVG de marca: un arco que va del
navy (tenue, se funde con el fondo) al dorado, con la cabeza dorada y su glow, y un
punto central claro.

Geometría tomada del SVG oficial (viewBox 120, círculo r=42 centrado en 60,60):
  - arranque del trazo arriba (12 en punto), cabeza arriba-izquierda.
  - hueco deliberado entre la cabeza y el arranque.
"""

from __future__ import annotations

import math

# Paleta del sitio (navy / dorado / paper)
NAVY = (14, 36, 57)        # #0E2439
NAVY_2 = (22, 50, 76)      # #16324C  (cola del cometa, casi se funde con el navy)
GOLD = (201, 162, 39)      # #C9A227
PAPER = (244, 246, 248)    # #F4F6F8

_HEAD_ANG = 200.0   # grados PIL (0 = este, horario, y hacia abajo) -> arriba-izquierda
_START_ANG = 270.0  # arriba (12 en punto)
_SWEEP = 290.0      # el trazo recorre 290° en sentido horario


def draw_comet(base, cx, cy, r, tail=NAVY_2, head=GOLD, dot=PAPER, width_ratio=0.12):
    """Compone el cometa sobre `base` (imagen RGBA), centrado en un círculo de radio r."""
    from PIL import Image, ImageDraw, ImageFilter

    W, H = base.size
    lw = max(2, int(round(r * width_ratio)))
    bbox = [cx - r, cy - r, cx + r, cy + r]
    hx = cx + r * math.cos(math.radians(_HEAD_ANG))
    hy = cy + r * math.sin(math.radians(_HEAD_ANG))

    # 1) glow de la cabeza (círculo dorado difuminado)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gr = r * 0.36
    gd.ellipse([hx - gr, hy - gr, hx + gr, hy + gr], fill=head + (90,))
    glow = glow.filter(ImageFilter.GaussianBlur(max(1.0, r * 0.15)))
    base.alpha_composite(glow)

    d = ImageDraw.Draw(base)

    # 2) el trazo, en segmentos con gradiente cola(navy)->cabeza(dorado)
    n = max(24, int(r))
    for i in range(n):
        a0 = _START_ANG + _SWEEP * i / n
        a1 = _START_ANG + _SWEEP * (i + 1) / n + 0.8
        t = i / (n - 1)
        col = tuple(int(round(tail[k] + (head[k] - tail[k]) * t)) for k in range(3))
        d.arc(bbox, a0, a1, fill=col + (255,), width=lw)

    # 3) cabeza dorada
    hr = max(2, r * 0.17)
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=head + (255,))

    # 4) punto central claro
    dr = max(1.0, r * 0.08)
    d.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=dot + (225,))

    return base
