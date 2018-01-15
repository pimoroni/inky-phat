#
# Python library to support the black/red IL91874 e-paper driver
#

import sys
import time
import atexit

import spidev

try:
    import RPi.GPIO as GPIO
except ImportError:
    sys.exit("This library requires the RPi.GPIO module\nInstall with: sudo pip install RPi.GPIO")

try:
    import numpy
except ImportError:
    sys.exit("This library requires the numpy module\nInstall with: sudo pip install numpy")

RESET_PIN = 27
BUSY_PIN = 17
DC_PIN = 22

MOSI_PIN = 10
SCLK_PIN = 11
CS0_PIN = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

_SPI_COMMAND = GPIO.LOW
_SPI_DATA = GPIO.HIGH


_V2_RESET = 0x12

_BOOSTER_SOFT_START = 0x06
_POWER_SETTING = 0x01
_POWER_OFF = 0x02
_POWER_ON = 0x04
_PANEL_SETTING = 0x00
_OSCILLATOR_CONTROL = 0x30
_TEMP_SENSOR_ENABLE = 0x41
_RESOLUTION_SETTING = 0x61
_VCOM_DC_SETTING = 0x82
_VCOM_DATA_INTERVAL_SETTING = 0x50
_DATA_START_TRANSMISSION_1 = 0x10
_DATA_START_TRANSMISSION_2 = 0x13
_DATA_STOP = 0x11
_DISPLAY_REFRESH = 0x12
_DEEP_SLEEP = 0x07

_PARTIAL_ENTER = 0x91
_PARTIAL_EXIT = 0x92
_PARTIAL_CONFIG = 0x90

_POWER_SAVE = 0xe3

WHITE = 0
BLACK = 1
RED = 2

class Inky212x104:

    def __init__(self, resolution=(104, 212), cs_pin=CS0_PIN, dc_pin=DC_PIN, reset_pin=RESET_PIN, busy_pin=BUSY_PIN, h_flip=False, v_flip=False):
        self.resolution = resolution
        self.width, self.height = resolution

        self.buffer = numpy.zeros((self.height, self.width), dtype=numpy.uint8)

        self.dc_pin = dc_pin
        self.reset_pin = reset_pin
        self.busy_pin = busy_pin
        self.cs_pin = cs_pin
        self.h_flip = h_flip
        self.v_flip = v_flip

        self.update_x1 = 0
        self.update_x2 = self.width
        self.update_y1 = 0
        self.update_y2 = self.height

        self.partial_mode = False
        self.partial_config = []
        self.border = 0b00000000

        GPIO.setup(self.dc_pin, GPIO.OUT, initial=GPIO.LOW, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(self.reset_pin, GPIO.OUT, initial=GPIO.HIGH, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(self.busy_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        GPIO.output(self.reset_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.reset_pin, GPIO.HIGH)
        time.sleep(0.1)

        if GPIO.input(self.busy_pin) == 1:
            self.set_version(1)
            self.palette = (BLACK, WHITE, RED)
        elif GPIO.input(self.busy_pin) == 0:
            self.set_version(2)
            self.palette = (WHITE, BLACK, RED)
        else:
            self.set_version(2)
            self.palette = (WHITE, BLACK, RED)

        self._spi = spidev.SpiDev()
        self._spi.open(0, self.cs_pin)
        self._spi.max_speed_hz = 488000

        atexit.register(self._display_exit)

    def set_version(self, version):
        if version not in (1, 2):
            raise ValueError("Version {} is not valid!".format(version))

        self.inky_version = version

        if version == 1:
            self._display_init = self._v1_init
            self._display_update = self._v1_update
            self._display_fini = self._v1_fini
            return

        if version == 2:
            self._display_init = self._v2_init
            self._display_update = self._v2_update
            self._display_fini = self._v2_fini
            return

    def _display_exit(self):
        self._display_fini()

    def _v2_fini(self):
        pass

    def _v2_update(self, buf_black, buf_red):
        self._send_command(0x44, [0x00, 0x0c]) # Set RAM X address
        self._send_command(0x45, [0x00, 0x00, 0xD3, 0x00, 0x00]) # Set RAM Y address + erroneous extra byte?

        self._send_command(0x04, [0x2d, 0xb2, 0x22]) # Source driving voltage control

        self._send_command(0x2c, 0x3c) # VCOM register, 0x3c = -1.5v?

        # Border control
        self._send_command(0x3c, 0x00)
        if self.border == 0b11000000:
            self._send_command(0x3c, 0x00)
        elif self.border == 0b01000000:
            self._send_command(0x3c, 0x33)
        elif self.border == 0b10000000:
            self._send_command(0x3c, 0xFF)

        VSS  = 0b00
        VSH1 = 0b01
        VSL  = 0b10
        VSH2 = 0b11
        def l(a, b, c, d):
            return (a << 6) | (b << 4) | (c << 2) | d

        ## Send LUTs
        self._send_command(0x32, [
        # Phase 0     Phase 1     Phase 2     Phase 3     Phase 4     Phase 5     Phase 6
        # A B C D     A B C D     A B C D     A B C D     A B C D     A B C D     A B C D
        0b01001000, 0b10100000, 0b00010000, 0b00010000, 0b00010011, 0b00000000, 0b00000000,# 0b00000000, # LUT0 - Black
        0b01001000, 0b10100000, 0b10000000, 0b00000000, 0b00000011, 0b00000000, 0b00000000,# 0b00000000, # LUTT1 - White
        0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,# 0b00000000, # IGNORE
        0b01001000, 0b10100101, 0b00000000, 0b10111011, 0b00000000, 0b00000000, 0b00000000,# 0b00000000, # LUT3 - Red
        0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000, 0b00000000,# 0b00000000, # LUT4 - VCOM
        #0xA5, 0x89, 0x10, 0x10, 0x00, 0x00, 0x00, # LUT0 - Black
        #0xA5, 0x19, 0x80, 0x00, 0x00, 0x00, 0x00, # LUT1 - White
        #0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # LUT2 - Red - NADA!
        #0xA5, 0xA9, 0x9B, 0x9B, 0x00, 0x00, 0x00, # LUT3 - Red
        #0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, # LUT4 - VCOM

#       Duration              |  Repeat
#       A     B     C     D   |
        67,   10,   31,   10,    4,  # 0 Flash
        16,   8,    4,    4,     6,  # 1 clear
        4,    8,    8,    32,    16,  # 2 bring in the black
        4,    8,    8,    64,    32, # 3 time for red
        6,    6,    6,    2,     2,  # 4 final black sharpen phase
        0,    0,    0,    0,     0,  # 4
        0,    0,    0,    0,     0,  # 5
        0,    0,    0,    0,     0,  # 6
        0,    0,    0,    0,     0   # 7
        ])

        self._send_command(0x44, [0x00, 0x0c]) # Set RAM X address
        self._send_command(0x45, [0x00, 0x00, 0xd3, 0x00]) # Set RAM Y address
        self._send_command(0x4e, 0x00) # Set RAM X address counter
        self._send_command(0x4f, [0x00, 0x00]) # Set RAM Y address counter

        self._send_command(0x24, buf_black)

        self._send_command(0x44, [0x00, 0x0c]) # Set RAM X address
        self._send_command(0x45, [0x00, 0x00, 0xd3, 0x00]) # Set RAM Y address
        self._send_command(0x4e, 0x00) # Set RAM X address counter
        self._send_command(0x4f, [0x00, 0x00]) # Set RAM Y address counter

        self._send_command(0x26, buf_red)


        self._send_command(0x22, 0xc7) # Display update setting
        self._send_command(0x20) # Display update activate
        time.sleep(0.05)
        self._busy_wait()

    def _v2_init(self):
        self.reset()

        self._send_command(0x74, 0x54) # Set analog control block
        self._send_command(0x75, 0x3b) # Sent by dev board but undocumented in datasheet

        # Driver output control
        self._send_command(0x01, [0xd3, 0x00, 0x00])

        # Dummy line period
        # Default value: 0b-----011
        # See page 22 of datasheet
        self._send_command(0x3a, 0x07)

        # Gate line width
        self._send_command(0x3b, 0x04)

        # Data entry mode
        self._send_command(0x11, 0x03)

    def _v1_fini(self):
        self._busy_wait()
        self._send_command(_VCOM_DATA_INTERVAL_SETTING, [0x00])
        self._send_command(_POWER_SETTING, [0x02, 0x00, 0x00, 0x00])
        self._send_command(_POWER_OFF)

    def _v1_update(self, buf_black, buf_red):
        # Start black data transmission
        self._send_command(_DATA_START_TRANSMISSION_1)
        self._send_data(buf_black)

        # Start red data transmission
        self._send_command(_DATA_START_TRANSMISSION_2)
        self._send_data(buf_red)

        self._send_command(_DISPLAY_REFRESH)

    def _v1_init(self):
        self.reset()

        self._busy_wait()    # Wait for driver to be ready to talk

        self._send_command(_POWER_SETTING, [0x07, 0x00, 0x0A, 0x00])
        self._send_command(_BOOSTER_SOFT_START, [0x07, 0x07, 0x07])
        self._send_command(_POWER_ON)

        self._busy_wait()    # Wait for driver to be ready to talk

        self._send_command(_PANEL_SETTING, [0b11001111])
        self._send_command(_VCOM_DATA_INTERVAL_SETTING, [0b00000111 | self.border]) # Set border to white by default

        self._send_command(_OSCILLATOR_CONTROL, [0x29])
        self._send_command(_RESOLUTION_SETTING, [0x68, 0x00, 0xD4])
        self._send_command(_VCOM_DC_SETTING, [0x0A])

        if self.partial_mode:
            self._send_command(_PARTIAL_CONFIG, self.partial_config)
            self._send_command(_PARTIAL_ENTER)
        else:
            self._send_command(_PARTIAL_EXIT)

    def clear_partial_mode(self):
        if self.inky_version == 1:
            self.partial_mode = False
            self.update_x1 = 0
            self.update_x2 = self.width
            self.update_y1 = 0
            self.update_y2 = self.height
        else:
            raise ValueError("This Inky pHAT display does not support partial updates")

    def set_partial_mode(self, vr_st, vr_ed, hr_st, hr_ed):
        if self.inky_version == 1:
            self.partial_mode = True
            self.update_x1 = (hr_st // 8) * 8 # Snap update region to byte boundary
            self.update_x2 = (hr_ed // 8) * 8
            self.update_y1 = vr_st
            self.update_y2 = vr_ed

            hr_ed -= 1
            vr_ed -= 1

            hr_st //= 8
            hr_ed //= 8

            if self.v_flip:
                _hr_st = ((self.width - 1) // 8) - hr_ed
                _hr_ed = ((self.width - 1) // 8) - hr_st
                hr_st = _hr_st
                hr_ed = _hr_ed

            if self.h_flip:
                _vr_st = self.height - 1 - vr_ed
                _vr_ed = self.height - 1 - vr_st
                vr_st = _vr_st
                vr_ed = _vr_ed

            # vr_st - vr_ed = 0 - 212 - Actually horizontal on Inky pHAT
            # hr_st - hr_ed = 0 - 12 - Actually vertical on Inky pHAT in 13 slices of 8 vertical pixels

            self.partial_config = [
                                                         # D7   D6   D5   D4   D3   D2   D1   D0
                0b00000000 | (hr_st & 0b11111) << 3,     #    HRST[7:3]             0    0    0
                0b00000111 | (hr_ed & 0b11111) << 3,     #    HRED[7:3]             1    1    1
                0b00000000 | (vr_st & 0b100000000) >> 8, # -    -    -    -    -    -    -   VRST[8]
                0b00000000 | (vr_st & 0b11111111),       #                VRST[7:0]
                0b00000000 | (vr_ed & 0b100000000) >> 8, # -    -    -    -    -    -    -   VRED[8]
                0b00000000 | (vr_ed & 0b11111111),       #                VRED[7:0]
                0b00000001,                              # -    -    -    -    -    -    -   PT_SCAN
            ]

            # HRST: Horizontal start channel bank: 00h to 13h (0 to 19)
            # HRED: Horizontal end channel bank: 00h to 13h (0 to 19), HRED must be greater than HRST
            # VRST: Vertical start line: 000h to 127h (0 to 295)
            # VRED: Vertical end line: 000h to 127h (0 to 295)
            # PT_SCAN: 0 = Only in partial window, 1 = inside and outside of partial window

        else:
            raise ValueError("This Inky pHAT display does not support partial updates")

    def set_border(self, border):
        if border in self.palette:
            c = self.palette[border]
            if c == BLACK:
                self.border = 0b11000000
            if c == RED:
                self.border = 0b01000000
            if c == WHITE:
                self.border = 0b10000000
        else:
            self.border = 0b00000000

    def set_palette(self, palette):
        self.palette = palette

    def update(self):
        self._display_init()

        x1, x2 = self.update_x1, self.update_x2
        y1, y2 = self.update_y1, self.update_y2

        region = self.buffer[y1:y2, x1:x2]

        if self.v_flip:
            region = numpy.fliplr(region)

        if self.h_flip:
            region = numpy.flipud(region)

        buf_red = numpy.packbits(numpy.where(region == RED, 1, 0)).tolist()
        if self.inky_version == 1:
            buf_black = numpy.packbits(numpy.where(region == 0, 0, 1)).tolist()
        else:
            buf_black = numpy.packbits(numpy.where(region == BLACK, 0, 1)).tolist()

        self._display_update(buf_black, buf_red)
        self._display_fini()

    def set_pixel(self, x, y, v):
        if v in self.palette:
            self.buffer[y][x] = self.palette[v]

    def _busy_wait(self):
        """Wait for the e-paper driver to be ready to receive commands/data.
        """
        wait_for = GPIO.HIGH
        if self.inky_version == 2:
            wait_for = GPIO.LOW

        while(GPIO.input(self.busy_pin) != wait_for):
            pass

    def reset(self):
        """Send a reset signal to the e-paper driver.
        """
        GPIO.output(self.reset_pin, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(self.reset_pin, GPIO.HIGH)
        time.sleep(0.1)

        if self.inky_version == 2:
            self._send_command(_V2_RESET)

        self._busy_wait()

    def _spi_write(self, dc, values):
        GPIO.output(self.dc_pin, dc)
        self._spi.xfer(values)

    def _send_command(self, command, data=None):
        self._spi_write(_SPI_COMMAND, [command])
        if data is not None:
            self._send_data(data)

    def _send_data(self, data):
        if isinstance(data, int):
            data = [data]
        o = ""
        for d in data:
            o += " {0:02x}".format(d)

        self._spi_write(_SPI_DATA, data)

