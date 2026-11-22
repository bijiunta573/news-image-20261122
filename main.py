#!/usr/bin/env python3
"""news-image-20261122: draw one 1024x1024 PNG summing up Sunday 22 November 2026.

Deterministic: no network, no clock, no randomness. stdlib + Pillow only.
Writes the image to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (23, 68, 128)
TEAL = (14, 110, 110)
GOLD = (176, 132, 24)
GREY = (90, 86, 78)
LINE = (18, 18, 18)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, text, fnt, fill, leading):
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, max_w, text, fnt, fill, leading):
    return para(draw, x, y, max_w, text, fnt, fill, leading)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=INK)
    d.text((32, 14), "THE WORLD IN ONE DAY", font=font(SERIF_B, 54),
           fill=(247, 243, 234))
    d.text((32, 78), "SUNDAY  22  NOVEMBER  2026", font=font(SANS_B, 26),
           fill=(232, 196, 90))
    d.text((688, 84), "make.fun  \u00b7  $100  \u00b7  TOP 50", font=font(SANS_B, 20),
           fill=(247, 243, 234))
    d.rectangle([0, 118, W, 122], fill=RED)

    # ---- hero: COP31 ----
    # globe panel on the left, headline + story on the right
    d.rectangle([28, 140, 996, 560], outline=INK, width=3)
    d.rectangle([28, 140, 996, 196], fill=RED)
    d.text((48, 150), "CLIMATE  \u00b7  ANTALYA, T\u00dcRKIYE", font=font(SANS_B, 26),
           fill=(255, 255, 255))
    # globe
    cx, cy, r = 200, 380, 130
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 130, 178),
              outline=INK, width=3)
    d.ellipse([cx - r + 34, cy - r + 30, cx - r + 120, cy - r + 92], fill=(46, 130, 70))
    d.ellipse([cx - 10, cy + 8, cx + 96, cy + 78], fill=(46, 130, 70))
    d.ellipse([cx - r + 60, cy + 62, cx + 20, cy + 118], fill=(46, 130, 70))
    d.arc([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14],
          start=200, end=340, fill=RED, width=10)
    d.text((cx - 118, cy + r + 22), "1.8\u00b0C  ABOVE  PRE-INDUSTRIAL",
           font=font(SANS_B, 20), fill=RED)
    # hero headline + copy
    x0 = 372
    y = headline(d, x0, 216, 600, "COP31: STILL NO DEAL", font(SANS_B, 54),
                 INK, 58)
    y = headline(d, x0, y + 8, 600, "36 hours into overtime",
                 font(SERIF_B, 32), RED, 38)
    y = para(d, x0, y + 12, 600,
             "Nearly 200 nations deadlocked in Antalya. The draft drops "
             "all fossil-fuel mentions and a $120bn adaptation fund. "
             "The EU: a good deal, or no deal. The US is absent "
             "for a second year.",
             font(SANS, 24), INK, 31)

    # ---- middle row: two stories ----
    d.rectangle([28, 580, 502, 800], outline=INK, width=3)
    d.rectangle([522, 580, 996, 800], outline=INK, width=3)
    d.rectangle([28, 580, 502, 622], fill=BLUE)
    d.rectangle([522, 580, 996, 622], fill=TEAL)
    d.text((44, 588), "DEFENCE", font=font(SANS_B, 24), fill=(255, 255, 255))
    d.text((538, 588), "SPORT", font=font(SANS_B, 24), fill=(255, 255, 255))
    headline(d, 44, 638, 440, "PENTAGON CURBS US\u2013CANADA TIES",
             font(SANS_B, 32), INK, 38)
    para(d, 44, 726, 440,
         "Hegseth's memo limits informal US\u2013Canada troop contact.",
         font(SANS, 23), INK, 29)
    headline(d, 538, 638, 440, "AUSTRALIA ENDS ENGLAND'S T20 RUN",
             font(SANS_B, 32), INK, 38)
    para(d, 538, 726, 440,
         "Australia break England's seven-match T20 winning streak.",
         font(SANS, 23), INK, 29)

    # ---- bottom row: three stories ----
    cols = [
        (28, 816, 316, "INDIA", GOLD, "MODI OPENS NITISH SETU",
         "New bridge links Patna and Vaishali."),
        (356, 816, 316, "WEATHER", BLUE, "CYCLONE AKVAN BITES",
         "14 flights cancelled at Ranchi airport."),
        (684, 816, 312, "TECH", TEAL, "TIKTOK'S DEEPFAKE SHIELD",
         "Global tool lets public figures spot fakes."),
    ]
    for (x, y0, w, tag, color, head, body) in cols:
        d.rectangle([x, y0, x + w, 962], outline=INK, width=3)
        d.rectangle([x, y0, x + w, y0 + 32], fill=color)
        d.text((x + 14, y0 + 4), tag, font=font(SANS_B, 20),
               fill=(255, 255, 255))
        headline(d, x + 14, y0 + 42, w - 28, head, font(SANS_B, 23), INK, 27)
        para(d, x + 14, y0 + 100, w - 28, body, font(SANS, 19), INK, 24)

    # ---- footer ----
    d.rectangle([0, 978, W, 982], fill=INK)
    d.text((28, 990),
           "Stories first reported or still developing on 22 Nov 2026  \u00b7  Sources: Reuters, AP, BBC",
           font=font(SANS, 20), fill=GREY)

    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    img.save(path, "PNG")
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
