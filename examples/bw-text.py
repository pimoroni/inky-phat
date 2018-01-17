#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inkyphat
import random
from PIL import ImageFont

font = ImageFont.truetype(inkyphat.fonts.FredokaOne, 22)

lines = random.randint(1,4)

message = '\n'.join([''.join([str(random.randint(1,10)) for x in range(random.randint(1,10))]) for y in range(lines)])
w, h = font.getsize(message)

x = 0
y = 0

inkyphat.text((x, y), message, inkyphat.BLACK, font)
inkyphat.show()
