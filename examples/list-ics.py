#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import calendar
import icalendar
import datetime

from PIL import Image, ImageFont

import inkyphat

print("""Inky pHAT: ICS Calendar Events List

Lists upcoming events from an ICS Calendar file.

""")

CALENDAR_FILE = "resources/test.ics"

#today = datetime.date.today()
today = datetime.date(2017,06,01)

inkyphat.set_border(inkyphat.BLACK)
#inkyphat.set_rotation(180)

inkyphat.rectangle((0, 0, inkyphat.WIDTH, inkyphat.HEIGHT), fill=inkyphat.BLACK)

ics = icalendar.Calendar.from_ical(open(CALENDAR_FILE).read())

font = inkyphat.ImageFont.truetype(inkyphat.fonts.FredokaOne, 12)

offset_x, offset_y = 10, 0

for item in ics.walk():
    if isinstance(item, icalendar.Event):
        dtstart = item['DTSTART'].dt
        dtend = item['DTEND'].dt
        summary = item['SUMMARY']

        if dtstart < today:
            continue

        text = "{}: {}".format(dtstart, summary)

        inkyphat.text((offset_x, offset_y), text, inkyphat.WHITE, font=font)

        offset_y += font.getsize(text)[1] + 2

        if offset_y >= inkyphat.HEIGHT:
            break

# And show it!
inkyphat.show()
