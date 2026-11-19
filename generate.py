"""Draw the front page of Thursday 19 November 2026 as one dense,
dramatic newspaper page: the Shenzhen trilateral summit leads, with
the ICJ genocide ruling, the Kerch Bridge strikes, the Gulf war,
the record Anthropic IPO, the record Van Gogh sale and COP31 below.
Deterministic: fixed text, fixed fonts, fixed layout, no randomness,
no timestamps. Output is a 1024x1024 PNG.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (243, 235, 214)
INK = (18, 18, 18)
RED = (178, 0, 27)
NAVY = (22, 34, 62)
GREY = (96, 89, 74)
PALE = (233, 220, 200)
GOLD = (176, 141, 42)
SUN = (214, 69, 65)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def load(name, size):
    """Load a DejaVu font at the requested size."""
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap_text(draw, text, font, max_width):
    """Split text into lines that fit max_width, word by word."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_font(draw, text, font_name, start_size, max_width, min_size=10):
    """Largest font size at which text still fits max_width."""
    size = start_size
    while size > min_size:
        font = load(font_name, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 1
    return load(font_name, min_size)


def draw_lines(draw, x, y, lines, font, fill=INK, leading=4):
    """Draw wrapped lines left-aligned; return the y below the block."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + leading
    return y


def rule(draw, x, y, width, weight=2, fill=INK):
    """A horizontal rule; return the y just below it."""
    draw.rectangle([x, y, x + width, y + weight - 1], fill=fill)
    return y + weight


def spaced(text):
    """Letterspace a short label the way newspaper kickers do."""
    return "   ".join(" ".join(word) for word in text.split())


def shrink_kicker(draw, text, font_name, start_size, max_width):
    """A letterspaced kicker shrunk until it fits the width."""
    size = start_size
    while size > 11:
        font = load(font_name, size)
        if draw.textlength(spaced(text), font=font) <= max_width:
            return font
        size -= 1
    return load(font_name, 11)


def star(draw, cx, cy, r, fill):
    """A five-pointed star centred at (cx, cy)."""
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        radius = r if i % 2 == 0 else r * 0.45
        points.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    draw.polygon(points, fill=fill)


def new_page():
    """A blank newsprint page with a double frame; return image, draw."""
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    draw.rectangle([18, 18, W - 19, H - 19], outline=INK, width=1)
    return img, draw


def masthead(draw):
    """Nameplate, date line and dateline cities; return y below it."""
    top = 28
    date_font = load(SANS_B, 17)
    draw.text((30, top), "THURSDAY, 19 NOVEMBER 2026",
              font=date_font, fill=INK)
    right = "THE DAY IN ONE PAGE"
    draw.text((994 - draw.textlength(right, font=date_font), top),
              right, font=date_font, fill=INK)
    y = rule(draw, 30, top + 26, 964, 3)
    name_font = fit_font(draw, "THE WORLD TODAY", SERIF_B, 66, 964)
    name_w = draw.textlength("THE WORLD TODAY", font=name_font)
    draw.text(((W - name_w) / 2, y + 2), "THE WORLD TODAY",
              font=name_font, fill=INK)
    y = y + 2 + name_font.size + 4
    y = rule(draw, 30, y, 964, 2)
    cities = "SHENZHEN  •  THE HAGUE  •  KYIV  •  RIYADH  •  NEW YORK  •  ANTALYA"
    city_font = load(SANS, 15)
    city_w = draw.textlength(cities, font=city_font)
    draw.text(((W - city_w) / 2, y + 4), cities, font=city_font, fill=GREY)
    return y + 4 + 15 + 6


def flag_us(draw, x, y, w, h):
    """A schematic Stars and Stripes."""
    stripe = h / 13
    for i in range(13):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                           fill=RED)
    canton_w, canton_h = w * 0.42, stripe * 7
    draw.rectangle([x, y, x + canton_w, y + canton_h], fill=NAVY)
    for row in range(4):
        for col in range(5):
            cx = x + 6 + col * (canton_w - 10) / 4
            cy = y + 6 + row * (canton_h - 10) / 3
            draw.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5],
                         fill=PAPER)


def flag_cn(draw, x, y, w, h):
    """A schematic Chinese flag: red field, five gold stars."""
    draw.rectangle([x, y, x + w, y + h], fill=RED)
    star(draw, x + w * 0.22, y + h * 0.28, h * 0.20, GOLD)
    for dx, dy in ((0.48, 0.12), (0.62, 0.24), (0.62, 0.44), (0.48, 0.54)):
        star(draw, x + w * dx, y + h * dy, h * 0.09, GOLD)


def flag_ru(draw, x, y, w, h):
    """A schematic Russian tricolour: white, blue, red bands."""
    draw.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 245))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def lead_scene(draw, x, y, w, h):
    """Three flags over a round table, red sun behind: the summit."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    flag_w, flag_h = 68, 40
    pole_h = 44
    spots = (x + 140, x + w // 2 - flag_w // 2, x + w - 140 - flag_w)
    painters = (flag_us, flag_cn, flag_ru)
    for fx, painter in zip(spots, painters):
        draw.line([fx + flag_w // 2, y + 6,
                   fx + flag_w // 2, y + 6 + pole_h], fill=INK, width=2)
        painter(draw, fx, y + 8, flag_w, flag_h)
    table_y = y + h - 18
    draw.ellipse([x + w // 2 - 150, table_y, x + w // 2 + 150,
                  table_y + 14], fill=NAVY)
    return y + h


def lead(draw, y):
    """The summit lead: kicker, headline, deck, scene, fact bar."""
    x, w = 30, 964
    kick_font = shrink_kicker(draw, "HISTORY IN SHENZHEN — THE FIRST-EVER TRILATERAL",
                              SANS_B, 20, w)
    draw.text((x, y), spaced("HISTORY IN SHENZHEN — THE FIRST-EVER TRILATERAL"),
              font=kick_font, fill=RED)
    y += kick_font.size + 8
    head_font = load(SERIF_B, 50)
    for line in ("TRUMP, XI AND PUTIN", "SIGN 'PEACE DECLARATION'"):
        while draw.textlength(line, font=head_font) > w:
            head_font = load(SERIF_B, head_font.size - 1)
        draw.text((x, y), line, font=head_font, fill=INK)
        y += head_font.size + 2
    y += 2
    deck = ("After a 90-minute meeting on the APEC sidelines, the three leaders "
            "pledge UN reform, no nuclear war — and more oil. Ukraine and Iran "
            "hang over the table.")
    deck_font = load(SANS, 20)
    y = draw_lines(draw, x, y, wrap_text(draw, deck, deck_font, w),
                   deck_font, leading=5)
    y += 6
    y = lead_scene(draw, x, y, w, 56)
    y += 8
    bar = "90 MINUTES  •  UN REFORM  •  NUCLEAR RESTRAINT  •  MORE OIL"
    bar_font = load(SANS_B, 19)
    while draw.textlength(bar, font=bar_font) > w - 24 and bar_font.size > 12:
        bar_font = load(SANS_B, bar_font.size - 1)
    draw.rectangle([x, y, x + w, y + 30], fill=INK)
    bar_w = draw.textlength(bar, font=bar_font)
    draw.text(((W - bar_w) / 2, y + 6), bar, font=bar_font, fill=PAPER)
    return y + 30 + 6


def art_scales(draw, x, y, width):
    """A small balance scale, centred in the column."""
    cx = x + width // 2
    draw.line([cx, y + 2, cx, y + 30], fill=INK, width=3)
    draw.line([cx - 26, y + 6, cx + 26, y + 6], fill=INK, width=3)
    draw.ellipse([cx - 3, y - 1, cx + 3, y + 5], fill=GOLD)
    for sx in (cx - 26, cx + 26):
        draw.line([sx, y + 6, sx, y + 16], fill=INK, width=2)
        draw.arc([sx - 12, y + 14, sx + 12, y + 30], 0, 180,
                 fill=INK, width=2)
        draw.line([sx - 12, y + 22, sx + 12, y + 22], fill=INK, width=2)
    draw.line([cx - 12, y + 30, cx + 12, y + 30], fill=INK, width=3)


def art_bridge(draw, x, y, width):
    """The Kerch Bridge with its middle span dropped into the strait."""
    deck_y = y + 8
    draw.rectangle([x, deck_y, x + width * 0.38, deck_y + 5], fill=INK)
    draw.rectangle([x + width * 0.62, deck_y, x + width, deck_y + 5],
                   fill=INK)
    draw.polygon([(x + width * 0.38, deck_y + 5),
                  (x + width * 0.50, deck_y + 16),
                  (x + width * 0.62, deck_y + 5)],
                 outline=INK, fill=(200, 190, 170))
    for tx in (x + width * 0.18, x + width * 0.80):
        draw.rectangle([tx - 3, y, tx + 3, deck_y + 5], fill=INK)
    for wy in (y + 26, y + 30):
        draw.line([x, wy, x + width, wy], fill=NAVY, width=2)


def art_bars(draw, x, y, width):
    """Three rising bars: the biggest IPO ever."""
    cx = x + width // 2
    heights = (10, 18, 26)
    for i, hgt in enumerate(heights):
        bx = cx - 42 + i * 30
        colour = RED if i == 2 else NAVY
        draw.rectangle([bx, y + 26 - hgt, bx + 20, y + 26], fill=colour)


def art_sun(draw, x, y, width):
    """A swirling Van Gogh sun in a frame."""
    cx = x + width // 2
    draw.rectangle([cx - 20, y, cx + 20, y + 28], outline=INK, width=2)
    draw.ellipse([cx - 9, y + 7, cx + 9, y + 21], fill=GOLD)
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1 = cx + 10 * math.cos(rad)
        y1 = y + 14 + 10 * math.sin(rad)
        x2 = cx + 14 * math.cos(rad)
        y2 = y + 14 + 14 * math.sin(rad)
        draw.line([x1, y1, x2, y2], fill=GOLD, width=2)


def art_globe(draw, x, y, width):
    """A globe with meridians: the climate talks."""
    cx, cy = x + width // 2, y + 14
    draw.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=NAVY, width=2)
    draw.ellipse([cx - 6, cy - 14, cx + 6, cy + 14], outline=NAVY, width=1)
    draw.line([cx - 14, cy, cx + 14, cy], fill=NAVY, width=1)
    draw.arc([cx - 14, cy - 8, cx + 14, cy + 8], 200, 340, fill=NAVY, width=1)


def column(draw, x, y, width, kicker, headline, deck, art, head_size=34,
           deck_size=18, art_h=52):
    """One story column: kicker, headline, deck, small drawing."""
    kick_font = shrink_kicker(draw, kicker, SANS_B, 16, width)
    draw.text((x, y), spaced(kicker), font=kick_font, fill=RED)
    y += kick_font.size + 6
    head_font = load(SERIF_B, head_size)
    y = draw_lines(draw, x, y, wrap_text(draw, headline, head_font, width),
                   head_font, leading=2)
    y += 3
    deck_font = load(SANS, deck_size)
    y = draw_lines(draw, x, y, wrap_text(draw, deck, deck_font, width),
                   deck_font, leading=4)
    y += 4
    art(draw, x, y, width)
    return y + art_h


def duo(draw, y):
    """Two half-page stories: the ICJ ruling and the Kerch Bridge."""
    col_w = 472
    y0 = y
    y_left = column(draw, 30, y, col_w, "THE HAGUE — WORLD COURT",
                    "MYANMAR GUILTY OF GENOCIDE",
                    "The ICJ finds the state responsible for the Rohingya "
                    "genocide — a first in its 80-year history. Decided 9–6.",
                    art_scales, head_size=32, deck_size=15, art_h=32)
    y_right = column(draw, 522, y, col_w, "KYIV — THIRD STRIKE IN A WEEK",
                     "KERCH BRIDGE HIT AGAIN",
                     "Missiles hit the rail span before the summit; a "
                     "227-metre road section already lies in the strait.",
                     art_bridge, head_size=32, deck_size=15, art_h=32)
    end = max(y_left, y_right)
    draw.line([512, y0 + 4, 512, end - 4], fill=GREY, width=1)
    return end + 4


def trio(draw, y):
    """Three stories across the page: IPO, Van Gogh, COP31."""
    col_w = 308
    y0 = y
    ends = []
    ends.append(column(draw, 30, y, col_w, "WALL STREET",
                       "$81.3BN — THE BIGGEST IPO IN HISTORY",
                       "Anthropic prices at $83; a $1.5 trillion value as ANT "
                       "joins Nasdaq.",
                       art_bars, head_size=22, deck_size=15, art_h=28))
    ends.append(column(draw, 358, y, col_w, "SOTHEBY'S, NEW YORK",
                       "$190.4M FOR A VAN GOGH",
                       "'Chataigniers en Fleurs' (1890) smashes the record. "
                       "Old mark: $117.2M.",
                       art_sun, head_size=22, deck_size=15, art_h=28))
    ends.append(column(draw, 686, y, col_w, "ANTALYA — COP31",
                       "HORMUZ: THE GREATEST THREAT IN HISTORY",
                       "The IEA warns as talks enter their final day; 21 points "
                       "unsettled.",
                       art_globe, head_size=22, deck_size=15, art_h=28))
    end = max(ends)
    for vx in (348, 676):
        draw.line([vx, y0 + 4, vx, end - 4], fill=GREY, width=1)
    return end + 4


def war_band(draw, y):
    """A red band for the Gulf war: the missile over Riyadh."""
    x, w = 30, 964
    kick_font = shrink_kicker(draw, "WAR IN THE GULF", SANS_B, 15, w - 32)
    head_font = load(SERIF_B, 30)
    deck_font = load(SANS, 16)
    deck = ("Windows blown out across seven floors of the kingdom's tallest "
            "tower — the second strike on the financial district in 11 days. "
            "Iran fires on Bahrain and Kuwait; US jets hit Qeshm Island.")
    lines = wrap_text(draw, deck, deck_font, w - 32)
    band_h = (6 + kick_font.size + 4 + head_font.size + 4
              + len(lines) * (deck_font.size + 4) + 6)
    draw.rectangle([x, y, x + w, y + band_h], fill=RED)
    inner = y + 6
    draw.text((x + 16, inner), spaced("WAR IN THE GULF"),
              font=kick_font, fill=(255, 220, 210))
    inner += kick_font.size + 4
    draw.text((x + 16, inner), "MISSILE HITS RIYADH'S PIF TOWER",
              font=head_font, fill=(255, 255, 255))
    inner += head_font.size + 4
    inner = draw_lines(draw, x + 16, inner, lines, deck_font,
                       fill=(255, 235, 230), leading=4)
    return y + band_h + 6


def footer(draw, y):
    """ALSO TODAY: four short items, then the closing line."""
    x, w = 30, 964
    y = rule(draw, x, y, w, 2)
    label_font = load(SANS_B, 14)
    draw.text((x, y + 6), "ALSO TODAY", font=label_font, fill=RED)
    y += 6 + 14 + 4
    items = ("NORTH KOREA EXPANDS URANIUM WORK AT YONGBYON, SAYS IAEA"
             "   •   BANGLADESH IN TURMOIL AS YUNUS HOME IS TORCHED"
             " — 28 DISTRICTS HIT"
             "   •   ISRAELI OPERATION IN CENTRAL GAZA"
             "   •   GTA VI LAUNCHES TODAY")
    item_font = load(SANS, 14)
    y = draw_lines(draw, x, y, wrap_text(draw, items, item_font, w),
                   item_font, leading=4)
    y += 4
    y = rule(draw, x, y, w, 1, fill=GREY)
    closing = ("THE WORLD TODAY  •  THURSDAY 19 NOVEMBER 2026  •  "
               "ALL THE NEWS THAT FITS ON ONE PAGE")
    close_font = load(SANS, 12)
    close_w = draw.textlength(closing, font=close_font)
    draw.text(((W - close_w) / 2, y + 4), closing, font=close_font,
              fill=GREY)
    return y + 4 + 12


def build(out_path):
    """Compose the whole page, section by section, and save it."""
    img, draw = new_page()
    y = masthead(draw)
    y = lead(draw, y)
    y = rule(draw, 30, y, 964, 2)
    y += 4
    y = duo(draw, y)
    y = rule(draw, 30, y, 964, 2)
    y += 4
    y = trio(draw, y)
    y = rule(draw, 30, y, 964, 2)
    y += 4
    y = war_band(draw, y)
    y = footer(draw, y)
    print("final y:", y)
    img.save(out_path, format="PNG")
    return out_path


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(target)
    print("wrote", target)



