"""Firmware has to run on MicroPython, but the simulator and tests run it
on CPython, which has more. Anything CPython-only only fails on the real
Pico, mid-run (2026-11-05: math.hypot froze the eyes)."""

import glob
import os
import re

ORGANS = os.path.join(os.path.dirname(__file__), "..", "..", "organs")
FIRMWARE_FILES = sorted(
    glob.glob(os.path.join(ORGANS, "*", "firmware", "*.py"))
    + glob.glob(os.path.join(ORGANS, "pico_common", "*.py"))
)

# What MicroPython v1.29's math module has on the Pico 2.
MICROPYTHON_MATH = {
    "acos", "acosh", "asin", "asinh", "atan", "atan2", "atanh", "ceil", "copysign",
    "cos", "cosh", "degrees", "e", "erf", "erfc", "exp", "expm1", "fabs", "floor",
    "fmod", "frexp", "gamma", "inf", "isclose", "isfinite", "isinf", "isnan", "ldexp",
    "lgamma", "log", "log10", "log2", "modf", "nan", "pi", "pow", "radians", "sin",
    "sinh", "sqrt", "tan", "tanh", "tau", "trunc",
}


def test_there_is_firmware_to_check():
    names = {os.path.basename(f) for f in FIRMWARE_FILES}
    assert {"expressions.py", "line_reader.py", "framebuffer.py"} <= names


def test_firmware_only_uses_math_that_micropython_has():
    used = {}
    for path in FIRMWARE_FILES:
        with open(path) as f:
            for name in re.findall(r"\bmath\.(\w+)", f.read()):
                used.setdefault(name, os.path.relpath(path, ORGANS))
    assert {name: where for name, where in used.items() if name not in MICROPYTHON_MATH} == {}


def test_no_two_organs_share_a_desktop_module_name():
    """Firmware imports its own files by bare name, and the virtual robot
    puts every organ's firmware folder on sys.path at once — so two organs
    with e.g. a panels.py would silently get each other's. Only main.py,
    which the desktop never imports, may repeat."""
    seen = {}
    for path in FIRMWARE_FILES:
        name = os.path.basename(path)
        if name in ("main.py", "__init__.py"):
            continue
        owner = os.path.relpath(os.path.dirname(path), ORGANS)
        assert name not in seen, f"{name} is in both {seen[name]} and {owner}"
        seen[name] = owner
