#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import calendar

from PIL import Image, ImageFont

import inkyphat


print("""Inky pHAT: Calendar

Draws a calendar for the current month to your Inky pHAT.

This example uses a sprite sheet of numbers and month names which are
composited over the background in a couple of different ways.

""")

inkyphat.set_border(inkyphat.BLACK)
inkyphat.set_rotation(180)

# Load our sprite sheet and prepare a mask
text = Image.open("resources/calendar.png")
text_mask = inkyphat.create_mask(text, [inkyphat.WHITE])

# Note: The mask determines which pixels from our sprite sheet we want
# to actually use when calling inkyphat.paste
# which uses PIL's Image.paste() method,
# See: http://pillow.readthedocs.io/en/3.1.x/reference/Image.html?highlight=paste#PIL.Image.Image.paste

# Load our backdrop image
inkyphat.set_image("resources/empty-backdrop.png")

# Grab the current date, and prepare our calendar
cal = calendar.Calendar()
now = datetime.datetime.now()
dates = cal.monthdatescalendar(now.year, now.month)

col_w = 20
col_h = 13

cols = 7
rows = len(dates) + 1

cal_w = 1 + ((col_w + 1) * cols)
cal_h = 1 + ((col_h + 1) * rows)

cal_x = inkyphat.WIDTH - cal_w - 2
cal_y = 2


def print_digit(position, digit, colour):
    """Print a single digit using the sprite sheet"""
    o_x, o_y = position
    
    num_margin = 2
    num_width = 6
    num_height = 7

    s_y = 11
    s_x = num_margin + (digit * (num_width + num_margin))

    sprite = text.crop((s_x, s_y, s_x + num_width, s_y + num_height))

    for x in range(num_width):
        for y in range(num_height):
            if sprite.getpixel((x, y)) == inkyphat.WHITE:
                inkyphat.putpixel((o_x + x, o_y + y), colour)

def print_number(position, number, colour):
    for digit in str(number):
        print_digit(position, int(digit), colour)
        position = (position[0] + 8, position[1])

# Paint out a black rectangle onto which we'll draw our canvas
inkyphat.rectangle((cal_x, cal_y, cal_x + cal_w - 1, cal_y + cal_h - 1), fill=inkyphat.BLACK, outline=inkyphat.WHITE)

# The starting position of the months in our spritesheet
months_x = 2
months_y = 20

# Number of months per row
months_cols = 3

# The width/height of each month in our spritesheet
month_w = 23
month_h = 9

# Figure out where the month is in the spritesheet
month_col = (now.month - 1) % months_cols
month_row = (now.month - 1) / months_cols

# Convert that location to usable X/Y coordinates
month_x = months_x + (month_col * month_w)
month_y = months_y + (month_row * month_h)

crop_region = (month_x, month_y, month_x + month_w, month_y + month_h)

month = text.crop(crop_region)
month_mask = text_mask.crop(crop_region)

monthyear_x = 28

# Paste in the month name we grabbed from our sprite sheet
inkyphat.paste(month, (monthyear_x, cal_y + 4), month_mask)

# Print the year right below the month
print_number((monthyear_x, cal_y + 5 + col_h), now.year, inkyphat.WHITE)



# Draw the vertical lines which separate the columns
# and also draw the day names into the table header
for x in range(cols):
    # Figure out the left edge of the column
    o_x = (col_w + 1) * x
    o_x += cal_x

    crop_x = 2 + (16 * x)

    # Crop the relevant day name from our text image
    crop_region = ((crop_x, 0, crop_x + 16, 9))
    day = text.crop(crop_region)
    day_mask = text_mask.crop(crop_region)
    inkyphat.paste(day, (o_x + 4, cal_y + 2), day_mask)

    # Offset to the right side of the column and draw the vertical line
    o_x += col_w + 1
    inkyphat.line((o_x, cal_y, o_x, cal_h))

# Draw the horizontal lines which separate the rows
for y in range(rows):
    o_y = (col_h + 1) * y
    o_y += cal_y + col_h + 1
    inkyphat.line((cal_x, o_y, cal_w + cal_x - 1, o_y))

# Step through each week
for row, week in enumerate(dates):
    y = (col_h + 1) * (row + 1)
    y += cal_y + 1

    # And each day in the week
    for col, day in enumerate(week):
        x = (col_w + 1) * col
        x += cal_x + 1

        # Draw in the day name.
        # If it's the current day, invert the calendar background and text
        if (day.day, day.month) == (now.day, now.month):
            inkyphat.rectangle((x, y, x + col_w - 1, y + col_h - 1), fill=inkyphat.WHITE)
            print_number((x+3, y+3), day.day, inkyphat.BLACK)

        # If it's any other day, paint in as white if it's in the current month
        # and red if it's in the previous or next month
        else:
            print_number((x+3, y+3), day.day, inkyphat.WHITE if day.month == now.month else inkyphat.RED)


# And show it!
inkyphat.show()
