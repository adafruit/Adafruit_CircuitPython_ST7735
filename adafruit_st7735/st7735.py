# The MIT License (MIT)
#
# Copyright (c) 2019 Scott Shawcroft and Melissa LeBlanc-Williams
#                    for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_st7735.st7735`
====================================================

Displayio driver for ST7735 based displays.

* Author(s): Scott Shawcroft and Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Hardware:**

* 1.8" SPI TFT display, 160x128 18-bit color:
  https://www.adafruit.com/product/618
* Adafruit 0.96" 160x80 Color TFT Display w/ MicroSD Card Breakout:
  https://www.adafruit.com/product/3533
* 1.8" Color TFT LCD display with MicroSD Card Breakout:
  https://www.adafruit.com/product/358
* Adafruit 1.44" Color TFT LCD Display with MicroSD Card breakout:
  https://www.adafruit.com/product/2088
* Adafruit Mini Color TFT with Joystick FeatherWing:
  https://www.adafruit.com/product/3321

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ST7735.git"

_INIT_SEQUENCE_B = (
    b"\x01\x80\x32" # _SWRESET and Delay 50ms
    b"\x11\x80\xFF" # _SLPOUT
    b"\x3A\x81\x05\x0A" # _COLMOD
    b"\xB1\x83\x00\x06\x03\x0A" # _FRMCTR1
    b"\x36\x01\x08" # _MADCTL
    b"\xB6\x02\x15\x02" # _DISSET5
    #1 clk cycle nonoverlap, 2 cycle gate, rise, 3 cycle osc equalize, Fix on VTL
    b"\xB4\x01\x00" # _INVCTR line inversion
    b"\xC0\x82\x02\x70\x0A" # _PWCTR1 GVDD = 4.7V, 1.0uA, 10 ms delay
    b"\xC1\x01\x05" # _PWCTR2 VGH = 14.7V, VGL = -7.35V
    b"\xC2\x02\x01\x02" # _PWCTR3 Opamp current small, Boost frequency
    b"\xC5\x82\x3C\x38\x0A" # _VMCTR1
    b"\xFC\x02\x11\x15" # _PWCTR6
    b"\xE0\x10\x09\x16\x09\x20\x21\x1B\x13\x19\x17\x15\x1E\x2B\x04\x05\x02\x0E" # _GMCTRP1 Gamma
    b"\xE1\x90\x0B\x14\x08\x1E\x22\x1D\x18\x1E\x1B\x1A\x24\x2B\x06\x06\x02\x0F\x0A" # _GMCTRN1
    b"\x2a\x00\x02\x00\x81" # _CASET
    b"\x2b\x00\x02\x00\x81" # _RASET
    b"\x13\x80\x0a" # _NORON
    b"\x29\x80\xFF" # _DISPON
)

_INIT_R1 = (
    b"\x01\x80\x96" # SWRESET and Delay 150ms
    b"\x11\x80\xff" # SLPOUT and Delay
    b"\xb1\x03\x01\x2C\x2D" # _FRMCTR1
    b"\xb2\x03\x01\x2C\x2D" # _FRMCTR2
    b"\xb3\x06\x01\x2C\x2D\x01\x2C\x2D" # _FRMCTR3
    b"\xb4\x01\x07" # _INVCTR line inversion
    b"\xc0\x03\xa2\x02\x84" # _PWCTR1 GVDD = 4.7V, 1.0uA
    b"\xc1\x01\xc5" # _PWCTR2 VGH=14.7V, VGL=-7.35V
    b"\xc2\x02\x0a\x00" # _PWCTR3 Opamp current small, Boost frequency
    b"\xc3\x02\x8a\x2a"
    b"\xc4\x02\x8a\xee"
    b"\xc5\x01\x0e" # _VMCTR1 VCOMH = 4V, VOML = -1.1V
    b"\x2a\x00" # _INVOFF
    b"\x36\x01\x18" # _MADCTL bottom to top refresh
    # 1 clk cycle nonoverlap, 2 cycle gate rise, 3 sycle osc equalie,
    # fix on VTL
    b"\x3a\x01\x05" # COLMOD - 16bit color
)

_INIT_R2_GREEN = (
    b"\x2a\x03\x02\x00\x81" # _CASET XSTART = 2, XEND = 129
    b"\x2b\x03\x02\x00\x81" # _RASET XSTART = 2, XEND = 129
)

_INIT_R2_RED = (
    b"\x2a\x00\x00\x00\x7F" # _CASET XSTART = 0, XEND = 127
    b"\x2b\x00\x00\x00\x9F" # _RASET XSTART = 0, XEND = 159
)

_INIT_R2_GREEN_144 = (
    b"\x2a\x00\x00\x00\x7F" # _CASET XSTART = 0, XEND = 127
    b"\x2b\x00\x00\x00\x7F" # _RASET XSTART = 0, XEND = 127
)

_INIT_R2_GREEN_160X80 = (
    b"\x2a\x00\x00\x00\x4F" # _CASET XSTART = 0, XEND = 79
    b"\x2b\x00\x00\x00\x9F" # _RASET XSTART = 0, XEND = 159
)

_INIT_R3 = (
    b"\xe0\x10\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2B\x39\x00\x01\x03\x10" # _GMCTRP1 Gamma
    b"\xe1\x10\x03\x1d\x07\x06\x2E\x2C\x29\x2D\x2E\x2E\x37\x3F\x00\x00\x02\x10" # _GMCTRN1
    b"\x13\x80\x0a" # _NORON
    b"\x29\x80\x64" # _DISPON
)

_INIT_R4_GREEN_160x80 = (
    b"\x36\x01\x68" # _MADCTL Rotate to Landscape Mode
)

_INIT_R4_BLACK = (
    b"\x36\x01\xC0" # _MADCTL Rotate to Landscape Mode
)

# pylint: disable=too-few-public-methods
class ST7735(displayio.Display):
    """ST7735 driver for ST7735R Green tabs"""
    def __init__(self, bus, *, width, height):
        _INIT_SEQUENCE = _INIT_R1 + _INIT_R2_GREEN + _INIT_R3
        super().__init__(bus, _INIT_SEQUENCE, width=width, height=height, colstart=2, rowstart=1)

class ST7735R_GREEN144(displayio.Display):
    """ST7735 driver for ST7735R Green tabs 1.44-inch"""
    def __init__(self, bus, *, width, height):
        _INIT_SEQUENCE = _INIT_R1 + _INIT_R2_GREEN + _INIT_R3
        super().__init__(bus, _INIT_SEQUENCE, width=width, height=height, colstart=2, rowstart=3)

class ST7735R_RED(displayio.Display):
    """ST7735 driver for ST7735R Red tabs"""
    def __init__(self, bus, *, width, height):
        _INIT_SEQUENCE = _INIT_R1 + _INIT_R2_RED + _INIT_R3
        super().__init__(bus, _INIT_SEQUENCE, width=width, height=height)

class ST7735R_BLACK(displayio.Display):
    """ST7735 driver for ST7735R Red tabs"""
    def __init__(self, bus, *, width, height):
        _INIT_SEQUENCE = _INIT_R1 + _INIT_R2_RED + _INIT_R3 + _INIT_R4_BLACK
        super().__init__(bus, _INIT_SEQUENCE, width=width, height=height)

class ST7735B(displayio.Display):
    """ST7735 driver for ST7735B"""
    def __init__(self, bus, *, width, height):
        super().__init__(bus, _INIT_SEQUENCE_B, width=width, height=height)

class MINI160X80(displayio.Display):
    """ST7735 driver for MINI160x80"""
    def __init__(self, bus):
        _INIT_SEQUENCE = _INIT_R1 + _INIT_R2_GREEN_160X80 + _INIT_R3 + _INIT_R4_GREEN_160x80
        super().__init__(bus, _INIT_SEQUENCE, width=160, height=80, rowstart=24)
