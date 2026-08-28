"""
Routes brain intents to the right organ driver. The brain never talks
to a transport or a Pico directly — it only knows organ names and
commands, so new organs can be added without touching brain code.
"""


class NervousSystem:
    def __init__(self):
        self._organs = {}

    def register(self, name: str, driver):
        """Attach an organ driver (anything implementing organs.base.Organ)."""
        self._organs[name] = driver

    def send(self, organ: str, cmd: str, **payload):
        driver = self._organs.get(organ)
        if driver is None:
            raise KeyError(f"No organ registered as '{organ}'")
        return driver.send_command(cmd, payload)

    def has_organ(self, name: str) -> bool:
        return name in self._organs
