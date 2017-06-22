#!/usr/bin/env python

from PIL import ImageFont

import inkyphat


font_file = inkyphat.fonts.FredokaOne
inkyphat.arc((0, 0, 212, 104), 0, 180, 2)

top = 0
left = 0
offset_left = 0

for font_size in (10, 12, 14, 16, 18, 20):
    text = "Test {}".format(font_size)
    font = inkyphat.ImageFont.truetype(font_file, font_size)
    width, height = font.getsize(text)
    inkyphat.text((0, top), text, 1, font=font)
    top += height + 1
    left = max(left, offset_left + width)

offset_left = left + 5
top = 0

for font_size in (22, 24, 26, 28):
    text = "Test {}".format(font_size)
    font = inkyphat.ImageFont.truetype(font_file, font_size)
    width, height = font.getsize(text)
    inkyphat.text((offset_left, top), text, 1, font=font)
    top += height + 1
    left = max(left, offset_left + width)

offset_left = left + 5
top = 0

for font_size in (30, 32, 34):
    text = "Test {}".format(font_size)
    font = inkyphat.ImageFont.truetype(font_file, font_size)
    width, height = font.getsize(text)
    inkyphat.text((offset_left, top), text, 1, font=font)
    top += height + 1
    left = max(left, offset_left + width)

inkyphat.show()
