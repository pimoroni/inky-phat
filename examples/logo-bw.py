#!/usr/bin/env python

from PIL import Image

import inkyphat

print("""Inky pHAT: Logo black and white

Displays the Inky pHAT logo in black and white.

""")

inkyphat.set_border(inkyphat.BLACK)
inkyphat.set_image(Image.open("InkyPhat-212x104-bw.png"))

inkyphat.show()
