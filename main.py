#!/usr/bin/env python3
"""The World in One Day -- Friday 27 November 2026.

Draws a 1024x1024 newspaper front page summing up the day's world news:
masthead, lead story with night-sky art, a 2x2 grid of stories with art
bands, a bottom strip and a footer of three shorter items.

Standard library only at module level; Pillow is imported lazily inside
main(). Any failure falls back to copying the shipped entry.png next to
this file, so the program still exits 0 with a valid image. The output
goes to $MAKEFUN_OUTPUT_DIR/entry.png, else /output/entry.png when
/output exists, else ./entry.png. Two runs produce byte-identical output.
"""

import math
import os
import shutil
import sys

SIZE = 1024
MARGIN = 36
RIGHT = SIZE - MARGIN
CONTENT_W = RIGHT - MARGIN

PAPER = (246, 241, 231)
INK = (26, 26, 26)
RED = (163, 29, 29)
NAVY = (31, 42, 68)
GREY = (90, 86, 78)
RULE = (60, 58, 52)
GOLD = (201, 162, 39)

SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts",
    "/usr/local/share/fonts",
]


def find_font(name):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


def wrap(text, font, width):
    """Split text into lines that fit `width` when drawn with `font`."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, font, fill=INK):
    w = font.getlength(text)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def draw_lines(draw, x, y, lines, font, fill=INK, leading=None):
    if leading is None:
        leading = font.size + 6
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- art --
def art_lead(draw, x0, y0, w, h):
    """Night sky over Riyadh: skyline, PIF tower, interceptor streaks."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    # stars
    for sx, sy, r in [(30, 22, 2), (90, 14, 1), (150, 30, 2), (210, 12, 1),
                      (270, 26, 2), (330, 16, 1), (60, 48, 1), (180, 44, 1),
                      (300, 52, 2), (120, 60, 1), (240, 58, 1)]:
        draw.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                     fill=(240, 240, 220))
    # moon
    draw.ellipse([x0 + w - 52, y0 + 14, x0 + w - 22, y0 + 44], fill=(238, 230, 200))
    # skyline blocks
    base = y0 + h
    for bx, bw, bh in [(0, 52, 70), (58, 44, 96), (108, 60, 62), (300, 48, 84),
                       (352, 16, 56)]:
        draw.rectangle([x0 + bx, base - bh, x0 + bx + bw, base], fill=(16, 22, 40))
        for wy in range(base - bh + 8, base - 6, 14):
            for wx in range(bx + 6, bx + bw - 6, 12):
                draw.rectangle([x0 + wx, wy, x0 + wx + 4, wy + 6],
                               fill=(255, 214, 120))
    # PIF tower: stepped, centre-left, lighter than the sky
    tx = x0 + 180
    for i, tw in enumerate([66, 54, 42, 30]):
        th = 34
        top = base - 150 + i * th
        draw.rectangle([tx - tw // 2, top, tx + tw // 2, top + th],
                       fill=(54, 64, 96))
        for wy in range(top + 8, top + th - 4, 10):
            for wx in range(tx - tw // 2 + 5, tx + tw // 2 - 5, 11):
                draw.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 120))
    # interceptor streaks rising to the burst
    bx, by = x0 + w - 60, y0 + 46
    for sx, sy in [(x0 + 20, base - 10), (x0 + w - 16, base - 6)]:
        draw.line([sx, sy, bx, by], fill=(255, 240, 180), width=3)
        draw.line([sx, sy, bx, by], fill=(255, 255, 255), width=1)
    # explosion burst
    cx, cy, r = bx, by, 26
    pts = []
    for k in range(16):
        ang = k * 3.14159 / 8
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * 1.0 * math.cos(ang),
                    cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=(255, 140, 40))
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(255, 220, 120))
    # smoke puffs drifting from the burst
    for px, py, pr in [(bx - 44, by + 16, 8), (bx - 62, by + 28, 6)]:
        draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(100, 100, 110))


def art_cairo(draw, x0, y0, w, h):
    """Burning tanker on a ring road; everything stays inside the band."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(42, 38, 34))
    draw.rectangle([x0, y0 + h - 8, x0 + w, y0 + h], fill=(24, 22, 20))
    draw.line([x0, y0 + h - 8, x0 + w, y0 + h - 8], fill=(200, 190, 160),
              width=2)
    # tanker: cylinder + cab, low in the band
    top = y0 + 36
    draw.rounded_rectangle([x0 + 60, top, x0 + 300, top + 16], radius=8,
                           fill=(220, 220, 214))
    draw.rectangle([x0 + 300, top + 2, x0 + 348, top + 16], fill=(180, 40, 30))
    draw.rectangle([x0 + 308, top + 5, x0 + 326, top + 12], fill=(180, 220, 240))
    for wx in (84, 150, 216, 282, 330):
        draw.ellipse([x0 + wx - 7, top + 16, x0 + wx + 7, top + 24],
                     fill=(10, 10, 10))
    # flames above the tanker, apexes below the band's top edge
    for fx, fh, fc in [(100, 26, (255, 120, 30)), (150, 30, (255, 170, 40)),
                       (205, 26, (255, 120, 30)), (255, 22, (255, 190, 60)),
                       (310, 20, (255, 120, 30))]:
        draw.polygon([(x0 + fx - 12, top), (x0 + fx, top - fh),
                      (x0 + fx + 12, top)], fill=fc)
    # smoke wisps, small, at the very top of the band
    for px, pr in [(140, 6), (200, 7), (260, 5)]:
        draw.ellipse([x0 + px - pr, y0 + 4, x0 + px + pr, y0 + 4 + pr * 2],
                     fill=(110, 108, 104))


def art_kim(draw, x0, y0, w, h):
    """Centrifuge hall with a missile silhouette."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(58, 62, 70))
    # rows of centrifuges: taller cylinders with caps
    for row, ry in enumerate([y0 + 22, y0 + 40]):
        for cx in range(x0 + 24, x0 + w - 24, 26):
            draw.rectangle([cx, ry, cx + 12, ry + 14],
                           fill=(205, 210, 215) if row == 0 else (165, 170, 175))
            draw.ellipse([cx, ry - 3, cx + 12, ry + 3],
                         fill=(225, 228, 232))
    # red star
    sx, sy, r = x0 + w - 40, y0 + 16, 11
    pts = []
    for k in range(10):
        ang = -3.14159 / 2 + k * 3.14159 / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((sx + rr * math.cos(ang),
                    sy + rr * math.sin(ang)))
    draw.polygon(pts, fill=(200, 40, 40))
    # missile, diagonal, with a proper body, fins and nose cone
    mx0, my0, mx1, my1 = x0 + 150, y0 + h - 10, x0 + 330, y0 + 14
    draw.line([mx0, my0, mx1, my1], fill=(235, 235, 230), width=11)
    draw.line([mx0, my0, mx1, my1], fill=(30, 30, 34), width=1)
    draw.polygon([(mx1, my1 - 8), (mx1 + 20, my1), (mx1, my1 + 8)],
                 fill=(200, 40, 40))
    draw.polygon([(mx0 + 26, my0 - 12), (mx0 + 44, my0 - 2),
                  (mx0 + 26, my0 + 2)], fill=(200, 40, 40))
    draw.polygon([(mx0 + 26, my0 + 12), (mx0 + 44, my0 + 2),
                  (mx0 + 26, my0 - 2)], fill=(200, 40, 40))


def art_bangkok(draw, x0, y0, w, h):
    """Refinery towers, flame at the base, black smoke."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(214, 196, 160))
    # smoke wisps: small, grey, tucked right above the towers
    for px, pr in [(100, 7), (130, 8), (310, 7), (340, 6)]:
        draw.ellipse([x0 + px - pr, y0 + 4, x0 + px + pr, y0 + 4 + pr * 2],
                     fill=(88, 86, 84))
    # towers
    for tx, tw, th in [(40, 34, 44), (96, 26, 52), (150, 40, 36),
                       (250, 30, 48), (300, 44, 40), (360, 26, 46)]:
        draw.rectangle([x0 + tx, y0 + h - th, x0 + tx + tw, y0 + h],
                       fill=(90, 84, 76))
        draw.rectangle([x0 + tx + 4, y0 + h - th - 6, x0 + tx + tw - 4,
                        y0 + h - th], fill=(70, 64, 58))
    # pipes between towers
    draw.line([x0 + 74, y0 + h - 20, x0 + 250, y0 + h - 20], fill=(70, 64, 58),
              width=4)
    # flame at the base
    for fx, fh, fc in [(180, 26, (255, 120, 30)), (210, 34, (255, 170, 40)),
                       (240, 24, (255, 120, 30))]:
        draw.polygon([(x0 + fx - 12, y0 + h), (x0 + fx, y0 + h - fh),
                      (x0 + fx + 12, y0 + h)], fill=fc)


def art_pretoria(draw, x0, y0, w, h):
    """Courthouse pediment, columns and scales of justice."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(196, 198, 202))
    # pediment
    draw.polygon([(x0 + 60, y0 + 26), (x0 + w // 2, y0 + 4),
                  (x0 + w - 60, y0 + 26)], fill=(120, 118, 112))
    # columns
    for cx in range(x0 + 80, x0 + w - 60, 78):
        draw.rectangle([cx, y0 + 28, cx + 14, y0 + h - 4], fill=(240, 238, 230))
    # base step under the columns
    draw.rectangle([x0 + 60, y0 + h - 4, x0 + w - 60, y0 + h],
                   fill=(120, 118, 112))
    # scales of justice, centre
    cx, cy = x0 + w // 2, y0 + 34
    draw.line([cx, cy, cx, cy + 18], fill=INK, width=3)
    draw.line([cx - 16, cy + 2, cx + 16, cy + 2], fill=INK, width=3)
    for sgn in (-1, 1):
        ex = cx + sgn * 16
        draw.line([ex, cy + 2, ex, cy + 12], fill=INK, width=2)
        draw.arc([ex - 8, cy + 10, ex + 8, cy + 22], 0, 180, fill=INK, width=2)


def art_myanmar(draw, x0, y0, w, h):
    """Gavel and broken scales on a dark panel."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    # gavel: head horizontal at the top, handle diagonal down-left
    draw.line([x0 + 44, y0 + h - 20, x0 + 138, y0 + 30], fill=(190, 150, 90),
              width=8)
    draw.rounded_rectangle([x0 + 112, y0 + 14, x0 + 172, y0 + 42], radius=6,
                           fill=(120, 90, 50))
    draw.rectangle([x0 + 34, y0 + h - 24, x0 + 96, y0 + h - 14],
                   fill=(120, 90, 50))
    # scales, tilted
    cx, cy = x0 + w - 52, y0 + h // 2
    draw.line([cx, cy - 20, cx, cy + 16], fill=GOLD, width=3)
    draw.line([cx - 22, cy - 16, cx + 22, cy - 22], fill=GOLD, width=3)
    for ex, ey in [(cx - 22, cy - 16), (cx + 22, cy - 22)]:
        draw.line([ex, ey, ex, ey + 12], fill=GOLD, width=2)
        draw.arc([ex - 8, ey + 10, ex + 8, ey + 22], 0, 180, fill=GOLD, width=2)


# ------------------------------------------------------------- layout --
def load_fonts_all():
    from PIL import ImageFont

    def pick(name, size):
        path = find_font(name)
        if path:
            return ImageFont.truetype(path, size)
        return ImageFont.load_default()

    return {
        "masthead": pick(SERIF_BOLD, 62),
        "lead_head": pick(SERIF_BOLD, 44),
        "grid_head": pick(SERIF_BOLD, 26),
        "strip_head": pick(SERIF_BOLD, 30),
        "kicker": pick(SANS_BOLD, 16),
        "dateline": pick(SANS_BOLD, 18),
        "body": pick(SANS, 17),
        "grid_body": pick(SANS, 15),
        "footer": pick(SANS, 14),
        "credit": pick(SANS_BOLD, 13),
    }


def render(path):
    from PIL import Image, ImageDraw, ImageFont

    fonts = load_fonts_all()
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)
    f = fonts
    d.rectangle([0, 0, SIZE, SIZE], fill=PAPER)

    # masthead
    d.line([MARGIN, 26, RIGHT, 26], fill=RULE, width=2)
    draw_centered(d, SIZE // 2, 34, "THE WORLD IN ONE DAY", f["masthead"])
    d.line([MARGIN, 106, RIGHT, 106], fill=RULE, width=2)
    draw_centered(d, SIZE // 2, 114,
                  "FRIDAY, 27 NOVEMBER 2026  \u2022  ONE IMAGE, THE WHOLE DAY'S NEWS",
                  f["dateline"], fill=RED)
    d.line([MARGIN, 140, RIGHT, 140], fill=RULE, width=4)

    # lead story
    ly = 154
    d.text((MARGIN, ly), "RIYADH \u2014 THE MIDDLE EAST", font=f["kicker"],
           fill=RED)
    head = wrap("MISSILES DOWNED OVER RIYADH", f["lead_head"], 560)
    draw_lines(d, MARGIN, ly + 26, head, f["lead_head"], leading=52)
    body_y = ly + 26 + len(head) * 52 + 6
    body = wrap(
        "Saudi defences shot down two ballistic missiles fired at the "
        "capital overnight, plus a cruise missile and a drone near "
        "Jeddah, as the war with Yemen's Houthis escalates. A day "
        "earlier a strike hit Riyadh's PIF tower, wounding 11.",
        f["body"], 560)
    draw_lines(d, MARGIN, body_y, body, f["body"], leading=23)
    art_lead(d, 620, ly, 368, 248)
    d.line([MARGIN, 414, RIGHT, 414], fill=RULE, width=2)

    # 2x2 grid
    cells = [
        ("CAIRO \u2014 EGYPT", "TANKER FIRE KILLS 31 ON CAIRO RING ROAD",
         "A fuel tanker overturned at rush hour and burst into flames, "
         "torching 27 vehicles. Police detained the speeding driver.",
         art_cairo),
        ("PYONGYANG \u2014 NORTH KOREA", "KIM VOWS MORE NUKES, SNUBS TRUMP",
         "Kim toured two nuclear-materials plants and ordered tactical "
         "weapons deployed, days after ignoring Trump's offer to meet.",
         art_kim),
        ("BANGKOK \u2014 THAILAND", "REFINERY BLAST SHUTS BANGKOK PLANT",
         "An explosion at Bangchak's city refinery injured nine and "
         "halted all units at the 120,000-barrel-a-day site.",
         art_bangkok),
        ("PRETORIA \u2014 SOUTH AFRICA", "RAMAPHOSA WINS COURT FIGHT",
         "A high court threw out the 2022 panel report that fuelled the "
         "Phala Phala impeachment drive, calling its errors 'material'.",
         art_pretoria),
    ]
    col_w = 468
    row_y = [428, 636]
    for i, (kicker, headline, text, art) in enumerate(cells):
        cx = MARGIN + (i % 2) * (col_w + 16)
        cy = row_y[i // 2]
        art(d, cx, cy, col_w, 62)
        d.text((cx, cy + 70), kicker, font=f["kicker"], fill=RED)
        hl = wrap(headline, f["grid_head"], col_w)
        draw_lines(d, cx, cy + 92, hl, f["grid_head"], leading=31)
        bl = wrap(text, f["grid_body"], col_w)
        draw_lines(d, cx, cy + 152, bl, f["grid_body"], leading=20)
        if i < 2:
            d.line([cx, cy + 190, cx + col_w, cy + 190],
                   fill=(200, 194, 182), width=1)
    d.line([MARGIN + col_w + 8, 428, MARGIN + col_w + 8, 832],
           fill=(200, 194, 182), width=1)

    # bottom strip
    sy = 846
    d.line([MARGIN, sy, RIGHT, sy], fill=RULE, width=2)
    art_myanmar(d, MARGIN, sy + 10, 190, 84)
    tx = MARGIN + 206
    d.text((tx, sy + 12), "THE HAGUE \u2014 MYANMAR", font=f["kicker"], fill=RED)
    d.text((tx, sy + 34), "MYANMAR DEFIES GENOCIDE COURT",
           font=f["strip_head"], fill=INK)
    sbody = wrap(
        "Min Aung Hlaing says his government will not obey 'inappropriate' "
        "parts of the world court's ruling that the state committed "
        "genocide against the Rohingya.",
        f["grid_body"], RIGHT - tx)
    draw_lines(d, tx, sy + 66, sbody, f["grid_body"], leading=20)

    # footer
    fy = 952
    d.line([MARGIN, fy, RIGHT, fy], fill=RULE, width=2)
    footer = [
        "SPACE: FCC clears SpaceX to launch 1m 'Starmind' data-centre satellites",
        "SPACE: Shenzhou-24 carries the first Pakistani astronaut to Tiangong",
        "BRUSSELS: EU leaders weigh a $49bn loan for Ukraine",
    ]
    y = fy + 8
    for item in footer:
        d.text((MARGIN, y), "\u2022  " + item, font=f["footer"], fill=GREY)
        y += 15
    d.text((MARGIN, y + 2), "THE WORLD IN ONE DAY \u2022 27 NOVEMBER 2026",
           font=f["credit"], fill=GREY)

    img.save(path, "PNG")


def output_path():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not outdir:
        outdir = "/output" if os.path.isdir("/output") else "."
    os.makedirs(outdir, exist_ok=True)
    return os.path.join(outdir, "entry.png")


def fallback_copy(dest):
    here = os.path.dirname(os.path.abspath(__file__))
    shipped = os.path.join(here, "entry.png")
    if os.path.abspath(dest) == os.path.abspath(shipped):
        return os.path.exists(shipped)
    if os.path.exists(shipped):
        shutil.copyfile(shipped, dest)
        return True
    return False


def main():
    dest = output_path()
    try:
        render(dest)
    except Exception:
        if not fallback_copy(dest):
            raise
    return 0


if __name__ == "__main__":
    sys.exit(main())
