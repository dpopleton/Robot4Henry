# Pico pin setup for the mouth's ST7789 panel — the wiring lives here and
# in the table in anatomy/mouth/build.md; keep the two the same. The
# pins are the left eye's (SPI0), so both organs' code reads alike.
# (Not called panels.py/backlight.py: the eyes have those, and the
# virtual robot can't load two modules with one name.)

from machine import Pin, PWM, SPI

from st7789 import ST7789

SCK, MOSI, DC, RST, CS, BL = 18, 19, 20, 21, 22, 16


class Backlight:
    def __init__(self, pin_no, level=1.0):
        self.pwm = PWM(Pin(pin_no))
        self.pwm.freq(1000)
        self.set(level)

    def set(self, level):
        """level in [0, 1] — 0 off, 1 full brightness."""
        level = max(0.0, min(1.0, level))
        self.pwm.duty_u16(int(level * 65535))


def init_panel(baudrate=40_000_000):
    """Returns (panel, backlight). If the picture is garbled, try
    baudrate=20_000_000 (frames then need ~100ms: raise TICK_MS)."""
    spi = SPI(0, baudrate=baudrate, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI))
    panel = ST7789(spi, cs=Pin(CS, Pin.OUT), dc=Pin(DC, Pin.OUT), rst=Pin(RST, Pin.OUT))
    return panel, Backlight(BL)
