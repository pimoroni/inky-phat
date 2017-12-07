#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inkyphat
import time
import sys

print("""Inky pHAT: Clean

Displays solid blocks of red, black, and white to clean the Inky pHAT
display of any screen burn.

Usage: {} <number of cycles>

""")

if len(sys.argv) > 1:
    cycles = int(sys.argv[1])
else:
    cycles = 3

colours = (inkyphat.RED, inkyphat.BLACK, inkyphat.WHITE)
colour_names= ("red", "black", "white")

for i in range(cycles):
    print("Cleaning cycle %i\n" % (i + 1))
    for j, c in enumerate(colours):
        print("- updating with %s" % colour_names[j])
        inkyphat.set_border(c)
        for x in range(inkyphat.WIDTH):
            for y in range(inkyphat.HEIGHT):
                inkyphat.putpixel((x, y), c)
        inkyphat.show()
        time.sleep(1)
    print("\n")

print("Cleaning complete!")
