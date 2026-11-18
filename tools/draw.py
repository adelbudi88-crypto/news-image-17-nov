#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news front page (1024x1024, Pillow only).

Run:  python3 tools/draw.py
Writes: entry.png next to the repository root (1024x1024, under 1 MiB).
All art is flat geometric shapes drawn with Pillow. No downloads, no AI.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "entry.png")

W = H = 1024
PAPER = (246, 241, 227)   # off-white newsprint
INK = (22, 35, 63)        # navy ink
NAVY = (27, 42, 74)
BRICK = (179, 64, 42)     # brick red
GOLD = (201, 162, 39)
TEAL = (42, 110, 122)
SKY = (214, 232, 240)
SEA = (58, 110, 150)
WHITE = (255, 255, 255)
GREY = (90, 96, 108)
LIGHT = (238, 232, 214)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
REG = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def wrap(draw, text, fnt, max_w):
    """Wrap text into lines that fit max_w pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    """Draw wrapped text, return y just below the block."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag(draw, x, y, label, fill=BRICK):
    """Small filled tag pill; returns (width, height)."""
    fnt = font(14, bold=True)
    tw = int(draw.textlength(label, font=fnt)) + 18
    th = 26
    draw.rounded_rectangle([x, y, x + tw, y + th], radius=4, fill=fill)
    draw.text((x + 9, y + 5), label, font=fnt, fill=WHITE)
    return tw, th


def star(draw, cx, cy, r_out, r_in, fill, points=8):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# ---- illustrations (flat geometric, drawn in a box x,y,w,h) ----

def ill_bridge(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # water
    draw.rectangle([x, y + h * 0.72, x + w, y + h], fill=SEA)
    for i in range(3):
        wy = y + h * (0.78 + i * 0.07)
        draw.arc([x + 8, wy - 6, x + w - 8, wy + 6], 0, 180, fill=WHITE, width=3)
    # deck
    dy = y + h * 0.62
    draw.rectangle([x + 6, dy, x + w - 6, dy + 10], fill=INK)
    # towers
    for tx in (x + w * 0.22, x + w * 0.68):
        draw.rectangle([tx - 5, y + h * 0.18, tx + 5, dy], fill=INK)
        draw.rectangle([tx - 16, y + h * 0.18, tx + 16, y + h * 0.24], fill=INK)
    # cables
    for tx in (x + w * 0.22, x + w * 0.68):
        draw.line([tx, y + h * 0.24, x + 10, dy], fill=INK, width=2)
        draw.line([tx, y + h * 0.24, x + w - 10, dy], fill=INK, width=2)
    # explosion above the deck, centre
    ex, ey = x + w * 0.47, y + h * 0.34
    draw.ellipse([ex - 22, ey - 40, ex + 4, ey - 20], fill=(120, 120, 120))
    star(draw, ex, ey, 34, 14, (240, 120, 30))
    star(draw, ex, ey, 20, 8, (250, 200, 60))


def ill_tanker(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h * 0.74, x + w, y + h], fill=SEA)
    # hull
    draw.polygon([(x + 8, y + h * 0.52), (x + w - 8, y + h * 0.52),
                  (x + w - 26, y + h * 0.74), (x + 26, y + h * 0.74)], fill=BRICK)
    draw.rectangle([x + 14, y + h * 0.40, x + 66, y + h * 0.52], fill=WHITE)
    draw.rectangle([x + 70, y + h * 0.44, x + 118, y + h * 0.52], fill=GOLD)
    # flames on deck
    for fx, fh in ((x + w * 0.62, 34), (x + w * 0.76, 26)):
        draw.polygon([(fx - 12, y + h * 0.52), (fx, y + h * 0.52 - fh),
                      (fx + 12, y + h * 0.52)], fill=(240, 120, 30))
        draw.polygon([(fx - 6, y + h * 0.52), (fx, y + h * 0.52 - fh + 12),
                      (fx + 6, y + h * 0.52)], fill=(250, 200, 60))
    # mine in the water
    mx, my = x + w * 0.18, y + h * 0.84
    for a in range(0, 360, 45):
        r = math.radians(a)
        draw.line([mx + 10 * math.cos(r), my + 10 * math.sin(r),
                   mx + 18 * math.cos(r), my + 18 * math.sin(r)],
                  fill=INK, width=3)
    draw.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=INK)
    # smoke above the flames
    draw.ellipse([x + w * 0.62, y + h * 0.28, x + w * 0.72, y + h * 0.40], fill=(120, 120, 120))
    draw.ellipse([x + w * 0.70, y + h * 0.24, x + w * 0.80, y + h * 0.36], fill=(150, 150, 150))


def ill_summit(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=LIGHT)
    # three flags on poles
    flags = [
        (BRICK, None),                 # China: red
        (None, "us"),                  # USA: stripes
        (None, "ru"),                  # Russia: white-blue-red
    ]
    fw, fh = w * 0.26, h * 0.30
    for i, (solid, kind) in enumerate(flags):
        fx = x + 8 + i * (fw + 8)
        fy = y + 10
        draw.line([fx + fw / 2, fy, fx + fw / 2, y + h * 0.78], fill=INK, width=3)
        if kind == "us":
            for s in range(4):
                draw.rectangle([fx, fy + s * fh / 4, fx + fw, fy + (s + 1) * fh / 4],
                               fill=BRICK if s % 2 == 0 else WHITE)
            draw.rectangle([fx, fy, fx + fw * 0.45, fy + fh * 0.5], fill=NAVY)
        elif kind == "ru":
            for s, col in enumerate([WHITE, (60, 110, 200), BRICK]):
                draw.rectangle([fx, fy + s * fh / 3, fx + fw, fy + (s + 1) * fh / 3], fill=col)
        else:
            draw.rectangle([fx, fy, fx + fw, fy + fh], fill=solid)
            star(draw, fx + 12, fy + 12, 7, 3, GOLD, points=5)
    # meeting table
    draw.ellipse([x + 10, y + h * 0.78, x + w - 10, y + h * 0.94], fill=(120, 74, 40))
    draw.rectangle([x + 10, y + h * 0.76, x + w - 10, y + h * 0.84], fill=(146, 94, 52))


def ill_radar(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # radar mast + tilted dish (flat polygon, no pieslice fan)
    cx, cy = x + w * 0.40, y + h * 0.58
    draw.rectangle([cx - 4, cy, cx + 4, y + h * 0.92], fill=INK)
    draw.polygon([(cx - 52, cy - 6), (cx - 8, cy - 52), (cx + 18, cy - 34),
                  (cx - 26, cy + 12)], fill=WHITE, outline=INK)
    draw.line([cx, cy, cx - 8, cy - 52], fill=INK, width=3)
    # signal arcs rising from the dish
    for r in (56, 70, 84):
        draw.arc([cx - r, cy - r - 18, cx + r, cy + r - 18], 300, 30, fill=TEAL, width=4)
    # drone top right, with a red intercept cross
    dx, dy = x + w * 0.80, y + h * 0.22
    draw.ellipse([dx - 15, dy - 6, dx + 15, dy + 6], fill=INK)
    draw.line([dx - 24, dy - 12, dx + 24, dy - 12], fill=INK, width=3)
    draw.line([dx - 24, dy + 12, dx + 24, dy + 12], fill=INK, width=3)
    draw.line([dx - 20, dy - 20, dx + 20, dy + 20], fill=BRICK, width=4)
    draw.line([dx - 20, dy + 20, dx + 20, dy - 20], fill=BRICK, width=4)


def ill_gavel(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=LIGHT)
    # document
    draw.rectangle([x + w * 0.08, y + h * 0.14, x + w * 0.58, y + h * 0.86],
                   fill=WHITE, outline=INK, width=2)
    for i in range(4):
        ly = y + h * (0.28 + i * 0.13)
        draw.line([x + w * 0.14, ly, x + w * 0.50, ly], fill=GREY, width=3)
    draw.text((x + w * 0.14, y + h * 0.16), "8", font=font(34, bold=True), fill=BRICK)
    # gavel: head + handle, diagonal
    hx, hy = x + w * 0.62, y + h * 0.30
    draw.polygon([(hx, hy), (hx + 52, hy - 22), (hx + 62, hy - 2), (hx + 10, hy + 20)],
                 fill=(120, 74, 40))
    draw.line([hx + 30, hy - 2, hx + 78, hy + 52], fill=(146, 94, 52), width=9)
    draw.ellipse([hx + 66, hy + 40, hx + 92, hy + 62], fill=GOLD)


def ill_jet(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun / clouds
    draw.ellipse([x + w * 0.72, y + 8, x + w * 0.88, y + 24], fill=GOLD)
    draw.ellipse([x + 10, y + 12, x + 52, y + 26], fill=WHITE)
    draw.ellipse([x + 34, y + 6, x + 76, y + 20], fill=WHITE)
    # jet silhouette, flying right
    cx, cy = x + w * 0.50, y + h * 0.55
    draw.polygon([(cx - 62, cy + 6), (cx + 52, cy - 8), (cx + 68, cy),
                  (cx + 52, cy + 8), (cx - 62, cy + 14)], fill=NAVY)
    draw.polygon([(cx - 10, cy), (cx + 18, cy - 34), (cx + 30, cy - 34),
                  (cx + 10, cy + 2)], fill=NAVY)
    draw.polygon([(cx - 16, cy + 10), (cx + 6, cy + 34), (cx + 18, cy + 34),
                  (cx + 2, cy + 12)], fill=NAVY)
    draw.polygon([(cx - 62, cy + 6), (cx - 78, cy - 6), (cx - 78, cy + 18),
                  (cx - 62, cy + 14)], fill=NAVY)
    # speed lines
    for i, ly in enumerate((0.30, 0.48, 0.66)):
        draw.line([x + 8, y + h * ly, x + 44, y + h * ly], fill=GREY, width=3)


def ill_pentagon(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=LIGHT)
    cx, cy = x + w * 0.50, y + h * 0.48
    r = min(w, h) * 0.36
    pts = []
    for i in range(5):
        a = -math.pi / 2 + 2 * math.pi * i / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=(150, 160, 175), outline=INK, width=3)
    inner = []
    for i in range(5):
        a = -math.pi / 2 + 2 * math.pi * i / 5
        inner.append((cx + r * 0.55 * math.cos(a), cy + r * 0.55 * math.sin(a)))
    draw.polygon(inner, fill=WHITE, outline=INK, width=2)
    # red X stamp over it
    draw.line([cx - 26, cy - 26, cx + 26, cy + 26], fill=BRICK, width=6)
    draw.line([cx - 26, cy + 26, cx + 26, cy - 26], fill=BRICK, width=6)


# ---- panels ----

def panel(draw, x, y, w, h, tag_label, headline, caption, ill, head_size=27,
          ill_frac=0.36, caption_size=16):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=3)
    ill_w = int(w * ill_frac)
    ill_x = x + w - ill_w - 12
    ill_y = y + 12
    ill_h = h - 24
    text_w = w - ill_w - 36
    tx = x + 14
    ty = y + 12
    tag(draw, tx, ty, tag_label)
    ty += 34
    fnt = font(head_size, bold=True)
    ty = text_block(draw, tx, ty, headline, fnt, INK, text_w,
                    leading=int(head_size * 1.10))
    ty += 4
    text_block(draw, tx, ty, caption, font(caption_size),
               (52, 58, 72), text_w, leading=caption_size + 4)
    # illustration, clipped to its box by drawing inside it
    ill(draw, ill_x, ill_y, ill_w, ill_h)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([6, 6, W - 7, H - 7], outline=NAVY, width=5)
    d.rectangle([16, 16, W - 17, H - 17], outline=GOLD, width=2)

    # ---- header band ----
    d.rectangle([22, 22, W - 23, 158], fill=NAVY)
    d.text((W // 2, 34), "17 NOVEMBER 2026", font=font(64, bold=True),
           fill=WHITE, anchor="ma")
    d.line([W // 2 - 300, 112, W // 2 + 300, 112], fill=GOLD, width=3)
    d.text((W // 2, 120), "THE WORLD IN ONE DAY", font=font(28, bold=True),
           fill=GOLD, anchor="ma")

    # ---- hero: Kerch Bridge ----
    hx, hy, hw, hh = 22, 170, W - 44, 224
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=WHITE, outline=INK, width=3)
    tag(d, hx + 14, hy + 12, "UKRAINE")
    d.text((hx + 14, hy + 46), "KERCH BRIDGE STRUCK AGAIN",
           font=font(33, bold=True), fill=INK)
    text_block(d, hx + 14, hy + 92,
               "Ukraine hits the Crimea bridge a second time in under 24 hours.",
               font(19), (52, 58, 72), 620, leading=24)
    text_block(d, hx + 14, hy + 144,
               "Russia hits Kyiv bridges over the Dnipro in reply.",
               font(19), (52, 58, 72), 620, leading=24)
    d.line([hx + 14, hy + 192, hx + 560, hy + 192], fill=GOLD, width=3)
    d.text((hx + 14, hy + 200), "SECOND STRIKE IN UNDER 24 HOURS",
           font=font(15, bold=True), fill=BRICK)
    ill_bridge(d, hx + hw - 312, hy + 12, 298, hh - 24)

    # ---- rows 2 and 3: two columns ----
    col_w = (W - 44 - 16) // 2
    x0, x1 = 22, 22 + col_w + 16
    panel(d, x0, 406, col_w, 168, "MIDDLE EAST",
          "TANKERS MINED NEAR HORMUZ",
          "Two tankers mined and burning; a third US carrier joins the region.",
          ill_tanker, head_size=26, caption_size=15)
    panel(d, x1, 406, col_w, 168, "ASIA",
          "XI, TRUMP, PUTIN TO MEET",
          "Three-way talks in Shenzhen on Thu 19 Nov, during the APEC summit.",
          ill_summit, head_size=26, caption_size=15)
    panel(d, x0, 586, col_w, 168, "MIDDLE EAST",
          "IRAN DRONE AT US RADAR",
          "Drone fired at US radar in Bahrain; intercepted, no casualties.",
          ill_radar, head_size=26, caption_size=15)
    panel(d, x1, 586, col_w, 168, "EUROPE",
          "UK SANCTIONS 8 ISRAELI FIRMS",
          "Over West Bank settlements; allies press Israel to open Gaza crossings.",
          ill_gavel, head_size=26, caption_size=15)

    # ---- bottom strip: Japan jets + Pentagon audit ----
    panel(d, x0, 766, col_w, 136, "ASIA",
          "JAPAN SCRAMBLES JETS",
          "Russian planes near Japan; Tokyo protests.",
          ill_jet, head_size=21, ill_frac=0.30, caption_size=15)
    panel(d, x1, 766, col_w, 136, "USA",
          "PENTAGON FAILS 9TH AUDIT",
          "Over $4.8T unverified, ninth year in a row.",
          ill_pentagon, head_size=21, ill_frac=0.30, caption_size=15)

    # ---- footer band ----
    d.rectangle([22, 914, W - 23, 1002], fill=NAVY)
    d.text((W // 2, 942), "17 NOVEMBER 2026  •  WORLD NEWS, ONE DAY, ONE IMAGE.",
           font=font(20, bold=True), fill=WHITE, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
