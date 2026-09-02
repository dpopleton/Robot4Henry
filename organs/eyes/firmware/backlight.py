# Both panels' BLK pins are tied to one shared GPIO (see README wiring
# table) — there's one brightness knob for both eyes, not per-eye control.

from machine import Pin, PWM

_FREQ = 1000


class Backlight:
    def __init__(self, pin_no: int):
        self.pwm = PWM(Pin(pin_no))
        self.pwm.freq(_FREQ)
        self.set(1.0)

    def set(self, level: float):
        """level in [0, 1] — 0 off, 1 full brightness."""
        level = max(0.0, min(1.0, level))
        self.pwm.duty_u16(int(level * 65535))
