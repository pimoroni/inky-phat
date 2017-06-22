#!/usr/bin/env python

from PIL import ImageFont
import sys

import inkyphat

print("""Inky pHAT: Hello... my name is:

Be patient! This example demonstrates partial updates,
and will take 30 seconds to display your name!

Hang in there...

""")

#inkyphat.set_rotation(180)

if len(sys.argv) < 2:
    print("Usage: {} <your name>".format(sys.argv[0]))
    sys.exit(1)

# Show the backdrop image

inkyphat.set_border(inkyphat.RED)
inkyphat.set_image("resources/hello-badge.png")
inkyphat.show()

# Add the text

font = ImageFont.truetype(inkyphat.fonts.AmaticSCBold, 38)

name = sys.argv[1]

w, h = font.getsize(name)

# Center the text and align it with the name strip

x = (inkyphat.WIDTH / 2) - (w / 2)
y = 71 - (h / 2)

inkyphat.text((x, y), name, inkyphat.BLACK, font)

# Refresh the text strip
#
# Partial updates are snapped to 8 pixel boundaries vertically,
# so the name strip is carefully aligned to an 8 pixel grid
#
# Generally you should refresh only whole horizontal rows. 
# Colours either side of the update area will be washed out!
#
# Your refreshed area may have a white border
# which could cut into surrounding colours.
#
# Remember:
# Art smartly to update partly!

inkyphat.set_partial_mode(56,96,0,inkyphat.WIDTH)
inkyphat.show()
