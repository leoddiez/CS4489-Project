#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FS = 15
font = ImageFont.truetype(FONT, FS)
fontb = ImageFont.truetype(FONT_B, FS)
title_font = ImageFont.truetype(FONT_B, 13)

BG = (13, 17, 23); BAR = (32, 37, 46)
WHITE = (220, 223, 228); GREY = (120, 128, 140)
GREEN = (63, 185, 80); RED = (248, 81, 73)
YELLOW = (210, 168, 58); CYAN = (86, 182, 194)
PAD_X = 18; PAD_TOP = 44; LINE_H = FS + 8


def color_for(s):
    low = s.lower()
    if s.startswith("$ #"):
        return [(s, GREY, False)]
    if s.startswith("$"):
        return [("$", GREEN, True), (s[1:], WHITE, False)]
    if s.strip().startswith("->"):
        if "200" in s:
            return [(s, GREEN, False)]
        if "401" in s:
            return [(s, RED, False)]
        return [(s, GREY, False)]
    if "second factor required" in low or "invalid second factor" in low or '"mfa_required"' in low:
        return [(s, RED, True)]
    if "login successful" in low:
        return [(s, YELLOW, True)]
    if '"role": "admin"' in s:
        return [(s, YELLOW, True)]
    return [(s, WHITE, False)]


def render(infile, outfile, title):
    with open(infile) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]
    cw = font.getbbox("M")[2]
    maxchars = max((len(l) for l in lines), default=40)
    W = max(PAD_X * 2 + cw * maxchars + 10, 560)
    H = PAD_TOP + PAD_X + LINE_H * len(lines) + 8
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, PAD_TOP - 8], fill=BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([16 + i * 22, 13, 30 + i * 22, 27], fill=c)
    tb = d.textbbox((0, 0), title, font=title_font)
    d.text(((W - (tb[2] - tb[0])) / 2, 12), title, font=title_font, fill=GREY)
    y = PAD_TOP
    for l in lines:
        x = PAD_X
        for text, col, bold in color_for(l):
            d.text((x, y), text, font=(fontb if bold else font), fill=col)
            x += (fontb if bold else font).getbbox(text)[2]
        y += LINE_H
    img.save(outfile)
    print(f"wrote {outfile} ({W}x{H})")


render("/home/claude/run/shots/cap_mfa.txt",
       "/home/claude/run/shots/05_admin_mfa_totp.png",
       "Terminal — admin MFA (TOTP) on defended backend")
