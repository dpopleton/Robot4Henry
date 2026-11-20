"""
Every organ the virtual robot can show (D-023). Each entry gives the
organ's virtual panel, its host driver and its bench controls; the app
does the rest (canvas, off/virtual/real/both switch, crash watch, a
command box for raw wire lines). Adding a body part means adding its
organs/<organ>/virtual.py and one entry here — see README.md.

The order here is the order of the benches in the window.
"""

from dataclasses import dataclass


@dataclass
class OrganKit:
    name: str
    panel_class: type       # (*drivers, one per SCREENS entry) -> write(bytes), tick(), redraw(), SCREENS, TICK_MS
    driver_class: type      # (transport) -> update(**kwargs)
    controls_class: type    # (parent, send, root, panel=panel) -> .frame, sync()
    example_command: str = ""


def _eyes():
    from organs.eyes.driver import EyesOrgan
    from organs.eyes.virtual import EyesControls, EyesPanel
    return OrganKit("eyes", EyesPanel, EyesOrgan, EyesControls, example_command="Ehappy:3 D-40,25")


def _mouth():
    from organs.mouth.driver import MouthOrgan
    from organs.mouth.virtual import MouthControls, MouthPanel
    return OrganKit("mouth", MouthPanel, MouthOrgan, MouthControls, example_command="S1 L80")


ORGANS = {
    "eyes": _eyes,
    "mouth": _mouth,
}
