# The MIT License (MIT)
#
# Copyright (c) 2019 Scott Shawcroft for Adafruit Industries LLC
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
`adafruit_ST7735`
====================================================

Displayio driver for ST7735 based displays.

* Author(s): Scott Shawcroft

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import displayio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ST7735.git"


_INIT_SEQUENCE = (
    b"\x01\x80\x96" # SWRESET
    b"\x11\x80\xff" # SLPOUT
    b"\xb1\x03\x01\x2C\x2D" # _FRMCTR1
    b"\xb2\x03\x01\x2C\x2D" #
    b"\xb3\x06\x01\x2C\x2D\x01\x2C\x2D"
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
    b"\xe0\x10\x02\x1c\x07\x12\x37\x32\x29\x2d\x29\x25\x2B\x39\x00\x01\x03\x10" # _GMCTRP1 Gamma
    b"\xe1\x10\x03\x1d\x07\x06\x2E\x2C\x29\x2D\x2E\x2E\x37\x3F\x00\x00\x02\x10" # _GMCTRN1
    b"\x2a\x03\x02\x00\x81" # _CASET XSTART = 2, XEND = 129
    b"\x2b\x03\x02\x00\x81" # _RASET XSTART = 2, XEND = 129
    b"\x13\x80\x0a" # _NORON
    b"\x29\x80\x64" # _DISPON
)

class ST7735(displayio.Display):
    """ST7735 driver for ST7735R Green tabs"""
    # TODO(tannewt): Add support for Red tabs and non-R chips. https://github.com/adafruit/Adafruit-ST7735-Library/blob/master/Adafruit_ST7735.cpp
    def __init__(self, bus, *, width, height):
        super().__init__(bus, _INIT_SEQUENCE, width=width, height=height, colstart=2)
