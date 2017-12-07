#!/usr/bin/env python

from PIL import Image

import inkyphat

inkyphat.set_border(inkyphat.BLACK)
inkyphat.set_image(Image.open("InkyPhat-212x104.png"))

inkyphat.show()
