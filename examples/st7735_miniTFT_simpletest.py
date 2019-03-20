import board
import displayio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_st7735 import st7735

reset_pin = 8
i2c = board.I2C()
ss = Seesaw(i2c, 0x5E)
ss.pin_mode(reset_pin, ss.OUTPUT)

spi = board.SPI()
tft_cs = board.D5
tft_dc = board.D6

displayio.release_displays()
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D9)

ss.digital_write(reset_pin, True)
display = st7735.MINI160x80(display_bus)
