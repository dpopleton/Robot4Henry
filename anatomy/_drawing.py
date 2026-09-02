"""Dimensioned 2D orthographic drawings — the printable counterpart to
generate.py's 3D solids.

cadquery can project a 3D shape into an orthographic SVG, but it has
no concept of a dimension line or a measurement label — that's a
manual drafting step in real CAD tools. Since every part here is
already fully parametric (measurements.yaml -> *_layout.py), it's more
reliable to draw the 2D views directly from those same numbers with
matplotlib than to reconstruct dimensions from a projected outline
after the fact. Each part's drawing.py calls these helpers to lay out
one or more views on an A4 sheet and save a PDF.
"""

import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

DIM_COLOR = "#c0392b"
OUTLINE_COLOR = "black"
FEATURE_COLOR = "#555555"


def new_sheet(part_name: str, view_titles: list[str]):
    """One row of orthographic views on an A4-landscape sheet."""
    fig, axes = plt.subplots(1, len(view_titles), figsize=(11.7, 8.3))
    if len(view_titles) == 1:
        axes = [axes]
    fig.suptitle(f"{part_name} — all dimensions in mm", fontsize=13, fontweight="bold")
    for ax, title in zip(axes, view_titles):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=10)
    return fig, axes


def outline_rect(ax, cx, cy, w, h, style="-", color=OUTLINE_COLOR, linewidth=1.2):
    ax.add_patch(
        Rectangle((cx - w / 2, cy - h / 2), w, h, fill=False, edgecolor=color, linewidth=linewidth, linestyle=style)
    )


def outline_circle(ax, cx, cy, r, style="-", color=OUTLINE_COLOR, linewidth=1.0):
    ax.add_patch(Circle((cx, cy), r, fill=False, edgecolor=color, linewidth=linewidth, linestyle=style))


def hidden_line(ax, x0, y0, x1, y1, color=FEATURE_COLOR):
    """A dashed line for a feature that's cut into a face, not a visible edge."""
    ax.plot([x0, x1], [y0, y1], color=color, linewidth=0.9, linestyle="--")


def dim_h(ax, x0, x1, y, label, offset=10):
    """Horizontal dimension between x0 and x1, drawn offset away from y."""
    yy = y - offset
    ax.annotate("", xy=(x1, yy), xytext=(x0, yy), arrowprops=dict(arrowstyle="<->", color=DIM_COLOR, linewidth=0.8))
    ax.plot([x0, x0], [y, yy], color=DIM_COLOR, linewidth=0.5, linestyle=":")
    ax.plot([x1, x1], [y, yy], color=DIM_COLOR, linewidth=0.5, linestyle=":")
    ax.text(
        (x0 + x1) / 2, yy, label, color=DIM_COLOR, fontsize=8, ha="center",
        va="top" if offset > 0 else "bottom", backgroundcolor="white",
    )


def dim_v(ax, y0, y1, x, label, offset=10):
    """Vertical dimension between y0 and y1, drawn offset away from x."""
    xx = x - offset
    ax.annotate("", xy=(xx, y1), xytext=(xx, y0), arrowprops=dict(arrowstyle="<->", color=DIM_COLOR, linewidth=0.8))
    ax.plot([x, xx], [y0, y0], color=DIM_COLOR, linewidth=0.5, linestyle=":")
    ax.plot([x, xx], [y1, y1], color=DIM_COLOR, linewidth=0.5, linestyle=":")
    ax.text(
        xx, (y0 + y1) / 2, label, color=DIM_COLOR, fontsize=8, ha="right" if offset > 0 else "left",
        va="center", rotation=90, backgroundcolor="white",
    )


def dim_diameter(ax, cx, cy, r, label, angle_deg=45, leader=12):
    a = math.radians(angle_deg)
    lx, ly = cx + r * math.cos(a), cy + r * math.sin(a)
    tx, ty = lx + leader * math.cos(a), ly + leader * math.sin(a)
    ax.plot([lx, tx], [ly, ty], color=DIM_COLOR, linewidth=0.6)
    ax.text(
        tx, ty, label, color=DIM_COLOR, fontsize=8,
        ha="left" if math.cos(a) >= 0 else "right", va="bottom" if math.sin(a) >= 0 else "top",
        backgroundcolor="white",
    )


def note(ax, x, y, text, **kw):
    ax.text(x, y, text, fontsize=7.5, color=FEATURE_COLOR, ha="center", **kw)


def autoscale(ax, points, margin=15):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)


def save_pdf(fig, generate_py_file: str, name: str) -> Path:
    folder = Path(generate_py_file).resolve().parent
    out_dir = folder / "exports"
    out_dir.mkdir(exist_ok=True)
    path = out_dir / f"{name}.pdf"
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(path)
    print(f"wrote {path}")
    return path
