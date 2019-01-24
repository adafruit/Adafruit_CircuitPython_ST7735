import adafruit_st7735
import board
import busio
import displayio
import time

displayio.release_displays()

spi = busio.SPI(board.SCL, board.SDA)
bus = displayio.FourWire(spi, chip_select=board.D9, command=board.D7, reset=board.D8)
display = adafruit_st7735.ST7735(bus, width=128, height=128)

s = displayio.Shape(10, 10)
p = displayio.Palette(2)
p[1] = 0xff0000
s = displayio.Sprite(s, pixel_shader=p, position=(0,0))
everything = displayio.Group(max_size=10)
everything.append(s)
display.show(everything)

time.sleep(10)
