# Shared geometry/color constants — used by the drawing logic (eyes.py,
# expressions.py) and by whatever's driving a display, real (gc9a01.py)
# or simulated (organs/eyes/simulate.py). Kept separate from eyes.py so
# expressions.py can import these without eyes.py and expressions.py
# importing each other.

WIDTH = 240
HEIGHT = 240

SCLERA_COLOR = 0xFFFF   # white, RGB565
PUPIL_COLOR = 0x0000    # black
BACKGROUND_COLOR = 0x0000

EYE_CENTER = (WIDTH // 2, HEIGHT // 2)
PUPIL_RADIUS = 42
MAX_PUPIL_OFFSET = 34
