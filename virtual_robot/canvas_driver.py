"""
Draws an organ's firmware output onto a Tk canvas.

- `CanvasDriver` is one screen: the same contract as the real panel
  drivers (fill, fill_circle, fill_polygon), scaled up for visibility and
  placed at its spot on the canvas. Each screen draws under its own tag,
  so fill() on one eye doesn't wipe the other.
- `CanvasScreens` is every screen of one organ on one canvas (the eyes
  have two, the mouth one). When covered it shows a note instead (the
  organ is off, or only on the real Pico) and the screens ignore drawing
  until uncovered.
"""


def rgb565_to_hex(color: int) -> str:
    r5, g6, b5 = (color >> 11) & 0x1F, (color >> 5) & 0x3F, color & 0x1F
    return f"#{r5 * 255 // 31:02x}{g6 * 255 // 63:02x}{b5 * 255 // 31:02x}"


class CanvasDriver:
    def __init__(self, canvas, width, height, scale=1.5, x=0, y=0, tag="screen0"):
        """width, height: the screen in panel pixels; x, y: where its
        top-left corner sits on the canvas, in panel pixels too."""
        self.canvas = canvas
        self.WIDTH, self.HEIGHT = width, height
        self.scale = scale
        self.x, self.y = x, y
        self.tag = tag
        self.covered = False

    def _xy(self, px, py):
        return (self.x + px) * self.scale, (self.y + py) * self.scale

    def fill(self, color: int):
        if self.covered:
            return
        self.canvas.delete(self.tag)
        self.canvas.create_rectangle(*self._xy(0, 0), *self._xy(self.WIDTH, self.HEIGHT),
                                     fill=rgb565_to_hex(color), outline="", tags=self.tag)

    def fill_circle(self, cx, cy, r, color: int):
        if self.covered:
            return
        self.canvas.create_oval(*self._xy(cx - r, cy - r), *self._xy(cx + r, cy + r),
                                fill=rgb565_to_hex(color), outline="", tags=self.tag)

    def fill_polygon(self, points, color: int):
        if self.covered:
            return
        flat = [coord for x, y in points for coord in self._xy(x, y)]
        self.canvas.create_polygon(flat, fill=rgb565_to_hex(color), outline="", tags=self.tag)


class CanvasScreens:
    def __init__(self, canvas, screens, scale=1.5):
        """screens: ((x, y, width, height), ...) in panel pixels, as a
        panel class's SCREENS. Makes one CanvasDriver per screen."""
        self.canvas = canvas
        self.scale = scale
        self.width = max(x + w for x, _y, w, _h in screens)
        self.height = max(y + h for _x, y, _w, h in screens)
        self.drivers = [CanvasDriver(canvas, w, h, scale, x, y, tag=f"screen{i}")
                        for i, (x, y, w, h) in enumerate(screens)]
        self.covered = False

    def cover(self, note):
        self.covered = True
        for driver in self.drivers:
            driver.covered = True
        self.canvas.delete("all")
        w, h = self.width * self.scale, self.height * self.scale
        self.canvas.create_rectangle(0, 0, w, h, fill="#303030", outline="")
        self.canvas.create_text(w / 2, h / 2, text=note, fill="#c0c0c0", width=w * 0.8, justify="center")

    def uncover(self):
        """The panel should redraw() straight after."""
        self.covered = False
        for driver in self.drivers:
            driver.covered = False
        self.canvas.delete("all")
