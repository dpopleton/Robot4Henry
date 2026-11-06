"""
Draws an organ's firmware output onto a Tk canvas: the same contract as
the real panel drivers (fill, fill_circle, fill_polygon), scaled up for
visibility. When `covered`, it shows a note instead (the organ is off,
or only on the real Pico) and ignores drawing until uncovered.
"""


def rgb565_to_hex(color: int) -> str:
    r5, g6, b5 = (color >> 11) & 0x1F, (color >> 5) & 0x3F, color & 0x1F
    return f"#{r5 * 255 // 31:02x}{g6 * 255 // 63:02x}{b5 * 255 // 31:02x}"


class CanvasDriver:
    def __init__(self, canvas, width, height, scale=1.5):
        self.canvas = canvas
        self.WIDTH, self.HEIGHT = width, height
        self.scale = scale
        self.covered = False

    def cover(self, note):
        self.covered = True
        self.canvas.delete("all")
        w, h = self.WIDTH * self.scale, self.HEIGHT * self.scale
        self.canvas.create_rectangle(0, 0, w, h, fill="#303030", outline="")
        self.canvas.create_text(w / 2, h / 2, text=note, fill="#c0c0c0", width=w * 0.8, justify="center")

    def uncover(self):
        self.covered = False

    def fill(self, color: int):
        if self.covered:
            return
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self.WIDTH * self.scale, self.HEIGHT * self.scale,
                                     fill=rgb565_to_hex(color), outline="")

    def fill_circle(self, cx, cy, r, color: int):
        if self.covered:
            return
        s = self.scale
        self.canvas.create_oval((cx - r) * s, (cy - r) * s, (cx + r) * s, (cy + r) * s,
                                fill=rgb565_to_hex(color), outline="")

    def fill_polygon(self, points, color: int):
        if self.covered:
            return
        flat = [coord * self.scale for p in points for coord in p]
        self.canvas.create_polygon(flat, fill=rgb565_to_hex(color), outline="")
