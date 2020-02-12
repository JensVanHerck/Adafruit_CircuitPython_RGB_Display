# The MIT License (MIT)
#
# Copyright (c) 2017 Radomir Dopieralski and Adafruit Industries
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
`adafruit_rgb_display.ili9341`
====================================================

A simple driver for the ILI9341/ILI9340-based displays.

* Author(s): Radomir Dopieralski, Michael McWethy
"""

try:
    import struct
except ImportError:
    import ustruct as struct

from adafruit_rgb_display.rgb import DisplaySPI

__version__ = "0.0.0-auto.0"


class SSD2119(DisplaySPI):
    """
    A simple driver for the SSD2119 based displays.

    >>> import busio
    >>> import digitalio
    >>> import board
    >>> from adafruit_rgb_display import color565
    >>> import adafruit_rgb_display.ili9341 as ili9341
    >>> spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    >>> display = ili9341.ILI9341(spi, cs=digitalio.DigitalInOut(board.GPIO0),
    ...    dc=digitalio.DigitalInOut(board.GPIO15))
    >>> display.fill(color565(0xff, 0x11, 0x22))
    >>> display.pixel(120, 160, 0)
    """

    _COLUMN_SET = 0x004F
    _PAGE_SET = 0x004E
    _RAM_WRITE = 0x0022
    _RAM_READ = 0x0022
    _INIT = (
        (0x0028, b'\x0006'),
        (0x0000, b'\x0001'),
        (0x0010, b'\x0000'),
        (0x0001, b'\x32EF'),
        (0x0002, b'\x0600'),
        (0x0003, b'\0x6A38'),  # Power Control 1, VRH[5:0]
        (0x0011, b'\x6870'),
        (0x000F,b'\x0000'),
        (0X000B,b'\x5308'),
        (0X000C, b'\x0003'),  # Power Control 2, SAP[2:0], BT[3:0]
        (0X000D, b'\x000A'),
        (0X000E, b'\x2E00'),
        (0x001E, b'\x00BE'),
        (0x0025, b'\x8000'),
        (0x0026, b'\x7800'),
        (0x004E, b'\x0000'),
        (0x004F, b'\x0000'),
        (0x0012, b'\x08D9'),
        (0x0030, b'\x0000'),
        (0x0031, b'\x0104'),
        (0x0032, b'\x0100'),
        (0x0033, b'\x0305'),
        (0x0034, b'\x0505'),
        (0x0035, b'\x0305'),
        (0x0036, b'\x0707'),
        (0x0037, b'\x0300'),
        (0x003A, B'\x1200'),
        (0x003B, B'\x0800'),
        (0x0007, B'\x0033'),
        (0x0022, None)
        
    )
    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"
    _DECODE_PIXEL = ">BBB"

    #pylint: disable-msg=too-many-arguments
    def __init__(self, spi, dc, cs, rst=None, width=320, height=240,
                 baudrate=16000000, polarity=0, phase=0, rotation=0):
        super().__init__(spi, dc, cs, rst=rst, width=width, height=height,
                         baudrate=baudrate, polarity=polarity, phase=phase,
                         rotation=rotation)
        self._scroll = 0
    #pylint: enable-msg=too-many-arguments

    def scroll(self, dy=None): #pylint: disable-msg=invalid-name
        """Scroll the display by delta y"""
        if dy is None:
            return self._scroll
        self._scroll = (self._scroll + dy) % self.height
        self.write(0x37, struct.pack('>H', self._scroll))
        return None
