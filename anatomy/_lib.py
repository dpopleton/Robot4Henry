"""Shared helpers for anatomy/*/generate.py scripts.

Each part's generate.py loads its own measurements.yaml, builds a
cadquery model from it, and calls export_all() to drop STEP + STL into
its exports/ folder. This module has no cadquery-specific model logic —
each generate.py owns its own shape — it just avoids repeating the
"load yaml relative to this file" and "export both formats" boilerplate
three times.
"""

from pathlib import Path

import cadquery as cq
import yaml


def load_measurements(generate_py_file: str) -> dict:
    """Load measurements.yaml from the same folder as the calling generate.py."""
    folder = Path(generate_py_file).resolve().parent
    path = folder / "measurements.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


def load_measurements_for(part: str) -> dict:
    """Load anatomy/<part>/measurements.yaml, for assembly scripts (e.g.
    anatomy/head/generate.py) that need another part's numbers — e.g. the
    head shell needs the eyes' plate footprint to cut a correctly sized
    window for it. Keeps each part's numbers defined in exactly one place.
    """
    anatomy_root = Path(__file__).resolve().parent
    path = anatomy_root / part / "measurements.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


def export_all(model: cq.Workplane, generate_py_file: str, name: str) -> None:
    """Export a model to <folder>/exports/<name>.step and .stl.

    STEP for re-opening in FreeCAD/Fusion/OnShape to keep editing,
    STL for slicing and printing directly.
    """
    folder = Path(generate_py_file).resolve().parent
    out_dir = folder / "exports"
    out_dir.mkdir(exist_ok=True)

    step_path = out_dir / f"{name}.step"
    stl_path = out_dir / f"{name}.stl"
    cq.exporters.export(model, str(step_path))
    cq.exporters.export(model, str(stl_path))
    print(f"wrote {step_path}")
    print(f"wrote {stl_path}")
