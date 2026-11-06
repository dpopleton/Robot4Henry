"""
OrganLink: one organ's switch between its virtual panel and its real
Pico (D-023). It's the transport the organ's driver writes to, and sends
each write wherever the switch says:

    off       nowhere — the panel is covered, the Pico untouched
    virtual   the panel only
    real      the real Pico only (the panel still follows, out of sight, so
              switching back shows the right state)
    both      the panel and the Pico, for side-by-side checks

While the real Pico is in use, poll_crash() watches its console
(nervous_system/pico_console.py) so a crash shows up instead of a freeze.
No Tk here, so it's tested without a window.
"""

from nervous_system.pico_console import PicoConsole

MODES = ("off", "virtual", "real", "both")
USES_PICO = ("real", "both")


class OrganLink:
    def __init__(self, panel, open_serial):
        """panel: has write(bytes). open_serial(port) returns a connected
        transport with write()/read_available()/close(), or raises
        OSError/ImportError."""
        self.panel = panel
        self.open_serial = open_serial
        self.mode = "virtual"
        self.port = None
        self._serial = None
        self._console = None

    def set_mode(self, mode, port=None):
        """Switch. Opening the Pico can fail (OSError, ImportError); the
        mode is then left as it was."""
        if mode not in MODES:
            raise ValueError(f"Unknown mode {mode!r}, use one of {MODES}")
        if mode in USES_PICO and (self._serial is None or port != self.port):
            self._close_serial()
            self._serial = self.open_serial(port)
            self._console = PicoConsole(self._serial)
            self.port = port
        elif mode not in USES_PICO:
            self._close_serial()
        self.mode = mode

    def drop_pico(self):
        """Back to virtual after the Pico crashed or vanished."""
        self._close_serial()
        self.mode = "virtual"

    def _close_serial(self):
        if self._serial is not None:
            try:
                self._serial.close()
            except OSError:
                pass
        self._serial = None
        self._console = None
        self.port = None

    # Transport side, for the organ's driver.
    def connect(self):
        pass

    def close(self):
        self._close_serial()

    def write(self, data: bytes):
        """Raises OSError if the Pico was unplugged; the panel has already
        had the bytes by then."""
        if self.mode == "off":
            return
        self.panel.write(data)
        if self.mode in USES_PICO:
            self._serial.write(data)

    def poll_crash(self):
        """(summary, full_text) once the Pico has crashed, else None."""
        return self._console.poll_crash() if self._console else None
