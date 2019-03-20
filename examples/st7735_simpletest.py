"""
This example will test out the display on the ST7735 Display
"""
import time
import board
import busio
import displayio
import adafruit_st7735.st7735 as st7735

displayio.release_displays()

spi = busio.SPI(board.SCL, board.SDA)
bus = displayio.FourWire(spi, chip_select=board.D9, command=board.D7, reset=board.D8)
display = st7735.ST7735(bus, width=128, height=128)

s = displayio.Shape(10, 10)
p = displayio.Palette(2)
p[1] = 0xff0000
s = displayio.TileGrid(s, pixel_shader=p, x=0, y=0)
everything = displayio.Group(max_size=10)
everything.append(s)
display.show(everything)

time.sleep(10)
