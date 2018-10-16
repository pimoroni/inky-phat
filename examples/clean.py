#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inkyphat
import time
import sys

print("""Inky pHAT: Clean

Displays solid blocks of red, black, and white to clean the Inky pHAT
display of any screen burn.

""".format(sys.argv[0]))

if len(sys.argv) < 2:
    print("""Usage: {} <colour> <number of cycles>
       Valid colours: red, yellow, black
""".format(sys.argv[0]))
    sys.exit(0)

colour = sys.argv[1].lower()

try:
    inkyphat.set_colour(colour)
except ValueError:
    print('Invalid colour "{}" for V{}\n'.format(colour, inkyphat.get_version()))
    if inkyphat.get_version() == 2:
        sys.exit(1)
    print('Defaulting to "red"')

if len(sys.argv) > 2:
    cycles = int(sys.argv[2])
else:
    cycles = 3

colours = (inkyphat.RED, inkyphat.BLACK, inkyphat.WHITE)
colour_names= (colour, "black", "white")

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
