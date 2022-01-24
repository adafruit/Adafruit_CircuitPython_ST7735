Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-st7735/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/st7735/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_ST7735/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_ST7735/actions/
    :alt: Build Status

displayio driver for ST7735B TFT-LCD displays.

Hardware
=========

This driver does not work for any current Adafruit Displays. It is intended to be used with displays
with an ST7735B or similar chipset and was created using initialization codes from the Arduino Library.
If you have a newer Adafruit Display with a ST7735R or ST7735S chip,
please visit `the Adafruit ST7735R Driver <https://github.com/adafruit/Adafruit_CircuitPython_ST7735R>`_.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython 4.0.0-beta.0+ <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

.. code-block:: python

    import board
    import displayio
    from adafruit_st7735 import ST7735

    spi = board.SPI()
    tft_cs = board.D5
    tft_dc = board.D6

    displayio.release_displays()
    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D9)

    display = ST7735(display_bus, width=128, height=128)

    # Make the display context
    splash = displayio.Group()
    display.show(splash)

    color_bitmap = displayio.Bitmap(128, 128, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFF0000

    bg_sprite = displayio.TileGrid(color_bitmap,
                                   pixel_shader=color_palette,
                                   x=0, y=0)
    splash.append(bg_sprite)

    while True:
        pass

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/st7735/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_ST7735/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
