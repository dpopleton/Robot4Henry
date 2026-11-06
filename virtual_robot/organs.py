"""
Every organ the virtual robot can show (D-023). Each entry gives the
organ's virtual panel, its host driver and its bench controls; the app
does the rest (canvas, off/virtual/real/both switch, crash watch, a
command box for raw wire lines). The eyes move here from
organs/eyes/simulate.py next (R-209).
"""

from dataclasses import dataclass


@dataclass
class OrganKit:
    name: str
    panel_class: type       # (driver) -> write(bytes), tick(), redraw(), WIDTH, HEIGHT, TICK_MS
    driver_class: type      # (transport) -> update(**kwargs)
    controls_class: type    # (parent, send, root) -> .frame, sync()
    example_command: str = ""


def _mouth():
    from organs.mouth.driver import MouthOrgan
    from organs.mouth.virtual import MouthControls, MouthPanel
    return OrganKit("mouth", MouthPanel, MouthOrgan, MouthControls, example_command="S1 L80")


ORGANS = {
    "mouth": _mouth,
}
