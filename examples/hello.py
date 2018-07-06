#!/usr/bin/env python

import sys

from PIL import ImageFont

import inkyphat

print("""Inky pHAT: Hello... my name is:

Use Inky pHAT as a personalised name badge!

""")

#inkyphat.set_rotation(180)

if len(sys.argv) < 3:
    print("""Usage: {} <your name> <colour>
       Valid colours for v2 are: red, yellow or black
       Inky pHAT v1 is only available in red.
""".format(sys.argv[0]))
    sys.exit(1)

colour = sys.argv[2]
inkyphat.set_colour(colour)

# Show the backdrop image

inkyphat.set_border(inkyphat.RED)
inkyphat.set_image("resources/hello-badge.png")

# Partial update if using Inky pHAT display v1

if inkyphat.get_version() == 1:
    inkyphat.show()

# Add the text

font = ImageFont.truetype(inkyphat.fonts.AmaticSCBold, 38)

name = sys.argv[1]

w, h = font.getsize(name)

# Center the text and align it with the name strip

x = (inkyphat.WIDTH / 2) - (w / 2)
y = 71 - (h / 2)

inkyphat.text((x, y), name, inkyphat.BLACK, font)

# Partial update if using Inky pHAT display v1

if inkyphat.get_version() == 1:
    inkyphat.set_partial_mode(56, 96, 0, inkyphat.WIDTH)

inkyphat.show()
