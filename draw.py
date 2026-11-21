#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261121.

A one-page newspaper front page that sums up the world news of
Saturday 21 November 2026. Everything is drawn from scratch with
Pillow primitives and the DejaVu fonts shipped with the system:
no downloaded pictures, no network, fully deterministic output.

Run:  python3 draw.py            (writes entry.png beside this file)
"""

import math
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234, 255)
INK = (17, 17, 17, 255)
RED = (178, 34, 34, 255)
NAVY = (18, 32, 62, 255)
GOLD = (201, 162, 39, 255)
GREY = (90, 88, 82, 255)
RULE = (120, 116, 106, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.25):
    lines = wrap(draw, text, fnt, width)
    lh = int(fnt.size * leading)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def burst(draw, cx, cy, r_out, r_in, n, fill):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def icon_scales(draw, x, y, s, col=INK):
    """Scales of justice."""
    draw.line([(x + s / 2, y + 6), (x + s / 2, y + s - 8)], fill=col, width=3)
    draw.line([(x + 6, y + 16), (x + s - 6, y + 16)], fill=col, width=3)
    for sx in (x + 10, x + s - 10):
        draw.line([(sx, y + 16), (sx, y + s - 22)], fill=col, width=2)
        draw.polygon(
            [(sx - 13, y + s - 22), (sx + 13, y + s - 22), (sx, y + s - 8)],
            outline=col, width=2)
    draw.line([(x + 14, y + s - 4), (x + s - 14, y + s - 4)], fill=col, width=3)


def icon_chart(draw, x, y, s, col=RED):
    draw.rectangle([x, y, x + s, y + s], outline=INK, width=2)
    pts = [(x + 8, y + 16), (x + s * 0.35, y + 26), (x + s * 0.55, y + 20),
           (x + s - 12, y + s - 12)]
    draw.line(pts, fill=col, width=4, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex - 12, ey - 2), (ex + 2, ey - 10), (ex + 4, ey + 4)],
                 fill=col)


def icon_flags(draw, x, y, s):
    # UK block (left half) and EU block (right half).
    draw.rectangle([x, y, x + s / 2 - 3, y + s], fill=(30, 60, 140, 255),
                   outline=INK, width=2)
    draw.line([(x, y + s / 2), (x + s / 2 - 3, y + s / 2)],
              fill=(255, 255, 255, 255), width=7)
    draw.line([(x + s / 4, y), (x + s / 4, y + s)],
              fill=(255, 255, 255, 255), width=7)
    draw.line([(x, y + s / 2), (x + s / 2 - 3, y + s / 2)],
              fill=(200, 30, 40, 255), width=3)
    draw.line([(x + s / 4, y), (x + s / 4, y + s)],
              fill=(200, 30, 40, 255), width=3)
    draw.rectangle([x + s / 2 + 3, y, x + s, y + s], fill=(0, 51, 153, 255),
                   outline=INK, width=2)
    for k in range(12):
        a = 2 * math.pi * k / 12 - math.pi / 2
        px = x + 3 * s / 4 + 0.32 * s * math.cos(a)
        py = y + s / 2 + 0.32 * s * math.sin(a)
        draw.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5],
                     fill=(255, 204, 0, 255))


def icon_globe(draw, x, y, s, col=(30, 110, 70, 255)):
    cx, cy, r = x + s / 2, y + s / 2, s / 2 - 2
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=col, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=col, width=2)
    draw.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55],
             200, 340, fill=col, width=2)


def icon_pill(draw, x, y, s, col=RED):
    # A capsule, tilted 45 degrees, drawn as two half-capsules.
    import PIL.Image as _I
    tmp = _I.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.rounded_rectangle([4, s / 2 - 11, s - 4, s / 2 + 11], radius=11,
                        fill=col)
    d.rounded_rectangle([s / 2, s / 2 - 11, s - 4, s / 2 + 11], radius=11,
                        fill=(255, 255, 255, 255), outline=col, width=2)
    tmp = tmp.rotate(45, resample=_I.BICUBIC, center=(s / 2, s / 2))
    draw._image.paste(tmp, (x, y), tmp)


def icon_numbers(draw, x, y, s):
    draw.text((x + 2, y + 2), "400+", font=font(SANS_B, 18), fill=RED)
    draw.text((x + 2, y + 28), "110", font=font(SANS_B, 18), fill=INK)


def skyline(draw, x0, y0, x1, y1):
    """Night sky over Kyiv: dark band, black rooftops, orange bursts,
    two missile arcs. y0..y1 is the band."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY)
    w = x1 - x0
    # stars
    for fx, fy in [(0.04, 0.12), (0.16, 0.30), (0.32, 0.10), (0.51, 0.26),
                   (0.69, 0.12), (0.86, 0.32), (0.95, 0.16), (0.42, 0.36),
                   (0.60, 0.40)]:
        sx, sy = x0 + fx * w, y0 + fy * (y1 - y0)
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255, 255))
    # missile arcs (dotted trails ending in a bright head)
    for (afx, bfx) in [(0.09, 0.28), (0.90, 0.69)]:
        ax, bx = x0 + afx * w, x0 + bfx * w
        ay, by = y1 - 8, y0 + 0.42 * (y1 - y0)
        steps = 24
        for i in range(steps + 1):
            t = i / steps
            px = ax + (bx - ax) * t
            py = ay + (by - ay) * t - 0.45 * (y1 - y0) * math.sin(math.pi * t)
            draw.ellipse([px - 2, py - 2, px + 2, py + 2],
                         fill=(255, 220, 120, 255))
        draw.ellipse([bx - 5, by - 5, bx + 5, by + 5],
                     fill=(255, 240, 180, 255))
    # bursts
    burst(draw, x0 + 0.28 * w, y0 + 0.52 * (y1 - y0), 40, 18, 10,
          (255, 140, 40, 255))
    burst(draw, x0 + 0.28 * w, y0 + 0.52 * (y1 - y0), 22, 10, 10,
          (255, 210, 90, 255))
    burst(draw, x0 + 0.69 * w, y0 + 0.55 * (y1 - y0), 33, 15, 10,
          (255, 140, 40, 255))
    burst(draw, x0 + 0.69 * w, y0 + 0.55 * (y1 - y0), 17, 8, 10,
          (255, 210, 90, 255))
    # skyline silhouettes
    base = y1
    bh = y1 - y0
    buildings = [(0.00, 0.55, 0.075, 0.45), (0.085, 0.66, 0.065, 0.34),
                 (0.16, 0.60, 0.09, 0.40), (0.26, 0.70, 0.06, 0.30),
                 (0.33, 0.62, 0.10, 0.38), (0.44, 0.68, 0.07, 0.32),
                 (0.52, 0.58, 0.095, 0.42), (0.625, 0.67, 0.065, 0.33),
                 (0.70, 0.61, 0.10, 0.39), (0.81, 0.68, 0.06, 0.32),
                 (0.88, 0.56, 0.085, 0.44), (0.975, 0.66, 0.025, 0.34)]
    for fx, fy, fw, fh in buildings:
        bx, by = x0 + fx * w, y0 + fy * bh
        bw = fw * w
        draw.rectangle([bx, by, bx + bw, base], fill=(8, 10, 18, 255))
        for wx in range(int(bx + 8), int(bx + bw - 6), 16):
            for wy in range(int(by + 10), base - 10, 18):
                if (wx * 7 + wy * 13) % 5 < 2:
                    draw.rectangle([wx, wy, wx + 5, wy + 7],
                                   fill=(255, 200, 90, 255))
    draw.text((x1 - 14, y0 + 8), "KYIV  ·  OVERNIGHT",
              font=font(SANS_B, 15), fill=(255, 255, 255, 255), anchor="ra")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    cw = W - 2 * mx              # content width

    # ---- Masthead -------------------------------------------------
    d.text((W / 2, 26), "THE WORLD IN ONE PICTURE",
           font=font(SERIF_B, 56), fill=INK, anchor="ma")
    d.text((W / 2, 96), "SATURDAY, 21 NOVEMBER 2026",
           font=font(SANS_B, 20), fill=RED, anchor="ma")
    d.line([(mx, 128), (W - mx, 128)], fill=INK, width=3)
    d.line([(mx, 133), (W - mx, 133)], fill=INK, width=1)

    # ---- Lead story ----------------------------------------------
    y = 148
    d.text((mx, y), "LEAD STORY  ·  UKRAINE  ·  POLAND",
           font=font(SANS_B, 17), fill=RED)
    y += 30
    y = para(d, mx, y,
             "RUSSIA'S BIGGEST STRIKE OF THE WAR HITS UKRAINE — AND LANDS IN POLAND",
             font(SERIF_B, 36), cw, leading=1.12)
    y += 6
    y = para(d, mx, y,
             "More than 400 drones and 110 missiles rain down overnight. "
             "At least eight are killed in Kyiv as bridges and rail stations "
             "are hit — and two missiles and a suspected drone come down in "
             "Poland. PM Tusk calls it a deliberate provocation.",
             font(SANS, 20), cw, leading=1.3)
    # The deck should end around y=385; illustration band is fixed.
    skyline(d, mx, 392, W - mx, 498)
    d.line([(mx, 508), (W - mx, 508)], fill=RULE, width=1)

    # ---- Grid: five stories + one numbers cell -------------------
    stories = [
        ("MYANMAR GUILTY OF GENOCIDE",
         "The International Court of Justice finds Myanmar responsible for "
         "genocide against the Rohingya — a landmark verdict cheered by survivors.",
         icon_scales),
        ("AI SELL-OFF: S&P IN CORRECTION",
         "US stocks fall 3.7% as the rout in AI and chip shares pushes the "
         "S&P 500 and the Dow into correction territory.",
         icon_chart),
        ("UK AND EU SIGN LANDMARK DEAL",
         "Leaders sign three agreements in Brussels on food exports, carbon "
         "markets and youth mobility — the biggest reset since Brexit.",
         icon_flags),
        ("COP31 TALKS RUN PAST DEADLINE",
         "The UN summit in Antalya, Turkey, stalls into overtime as nearly "
         "200 nations fail to agree on fossil fuels.",
         icon_globe),
        ("CANCER PILL MAKES TUMOURS VANISH",
         "Daraxonrasib, a trial pill for pancreatic cancer, made tumours "
         "undetectable on scans in one in 12 patients.",
         icon_pill),
        ("THE DAY IN NUMBERS",
         "400+ drones and 110 missiles fired at Ukraine · 3.7% fall on US "
         "stocks · 25 European countries see Gen Z protests.",
         icon_numbers),
    ]
    gx, gy = mx, 528
    cell_w = (cw - 2 * 18) // 3
    cell_h = 196
    for i, (head, body, icon) in enumerate(stories):
        r, c = divmod(i, 3)
        x = gx + c * (cell_w + 18)
        yy = gy + r * (cell_h + 14)
        icon(d, x, yy, 54)
        # Headline, wrapped to at most two lines beside the icon.
        hlines = wrap(d, head, font(SANS_B, 19), cell_w - 66)
        hy = yy + 2
        for ln in hlines[:2]:
            d.text((x + 66, hy), ln, font=font(SANS_B, 19), fill=INK)
            hy += 24
        by = yy + 62
        para(d, x, by, body, font(SANS, 16), cell_w, leading=1.28)
        if c < 2:
            d.line([(x + cell_w + 9, yy + 4), (x + cell_w + 9, yy + cell_h - 8)],
                   fill=RULE, width=1)
    d.line([(mx, 936), (W - mx, 936)], fill=INK, width=2)

    # ---- Also today + footer --------------------------------------
    y = 948
    para(d, mx, y,
         "ALSO TODAY:  Voyager 1 becomes the first human-made object one "
         "light-day from Earth  ·  Houthi strike damages Riyadh's tallest "
         "tower, the PIF tower — no one hurt  ·  FBI crime database "
         "reportedly hacked.",
         font(SANS, 15), cw, leading=1.3)
    d.text((mx, 1002), "Sources: Reuters · AP · France 24 · BBC · CBS News — 21 November 2026",
           font=font(SANS, 12), fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
