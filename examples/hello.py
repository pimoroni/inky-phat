#!/usr/bin/env python

from PIL import ImageFont
import sys

import inkyphat

if len(sys.argv) < 2:
    print("Usage: {} <your name>".format(sys.argv[0]))
    sys.exit(1)

inkyphat.set_border(inkyphat.RED)
inkyphat.set_image("resources/hello-badge.png")

font = ImageFont.truetype(inkyphat.fonts.AmaticSCBold, 38)

name = sys.argv[1]
w, h = font.getsize(name)
x = (inkyphat.WIDTH / 2) - (w / 2)
y = 71 - (h / 2)

inkyphat.text((x, y), name, inkyphat.BLACK, font)


inkyphat.set_partial_mode(0,103,0,211)
inkyphat.show()

inkyphat.set_partial_mode(56,88,0,211)
inkyphat.show()
