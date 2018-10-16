#!/usr/bin/env python

from PIL import Image
import sys

import inkyphat

print("""Inky pHAT: Logo

Displays the Inky pHAT logo.

""")

if len(sys.argv) < 2:
    print("""Usage: {} <colour>
       Valid colours: red, yellow, black
""".format(sys.argv[0]))
    sys.exit(0)

colour = sys.argv[1].lower()

try:
    inkyphat.set_colour(colour)
except ValueError:
    print('Invalid colour "{}" for V{}\n'.format(colour, inkyphat.get_version()))
    sys.exit(1)

inkyphat.set_border(inkyphat.BLACK)

if colour == 'black':
    inkyphat.set_image(Image.open("InkyPhat-212x104-bw.png"))
else:
    inkyphat.set_image(Image.open("InkyPhat-212x104.png"))


inkyphat.show()
