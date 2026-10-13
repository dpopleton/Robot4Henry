import time
import threading
import config.settings as settings


class SessionManager:
    def __init__(self, on_session_end, timeout_seconds: int = None):
        """
        on_session_end: callback fired when inactivity timeout is reached.
        timeout_seconds: override for testing, otherwise uses settings.
        """
        self.on_session_end = on_session_end
        self._timeout_seconds = timeout_seconds
        self._last_activity = time.time()
        self._active = False
        self._in_turn = False
        self._timer = None
        self._lock = threading.Lock()

    def _get_timeout(self) -> int:
        if self._timeout_seconds is not None:
            return self._timeout_seconds
        return settings.SESSION_TIMEOUT_SECONDS

    def record_activity(self):
        """Call this on every exchange."""
        with self._lock:
            self._last_activity = time.time()
            self._active = True
            self._reset_timer()

    def begin_turn(self) -> bool:
        """Mark the session active and hold off the timeout until
        end_turn().  A reply can take seconds on the robot laptop, so a
        message that arrives just before the timeout must not be cut in two.

        Returns whether the session was already active.
        """
        with self._lock:
            was_active = self._active
            self._active = True
            self._in_turn = True
            if self._timer:
                self._timer.cancel()
                self._timer = None
            return was_active

    def end_turn(self):
        """The turn is over (whether or not it succeeded): restart the clock."""
        with self._lock:
            self._in_turn = False
            self._last_activity = time.time()
            if self._active:
                self._reset_timer()

    def _reset_timer(self):
        if self._timer:
            self._timer.cancel()
        self._timer = threading.Timer(
            self._get_timeout(),
            self._handle_timeout
        )
        self._timer.daemon = True
        self._timer.start()

    def _handle_timeout(self):
        with self._lock:
            # A timer that was already firing as a turn began; end_turn()
            # starts a fresh one.
            if not self._active or self._in_turn:
                return
            self._active = False
            self._timer = None
        self.on_session_end()

    def is_active(self) -> bool:
        with self._lock:
            return self._active

    def end_session_manually(self, notify: bool = True) -> bool:
        """End an active session once.

        Returns whether there was a session to end.  ``notify=False`` lets
        callers that need synchronous cleanup perform it themselves without
        recursively invoking the timeout callback.
        """
        with self._lock:
            if not self._active:
                return False
            if self._timer:
                self._timer.cancel()
                self._timer = None
            self._active = False
        if notify:
            self.on_session_end()
        return True

    def stop(self):
        with self._lock:
            if self._timer:
                self._timer.cancel()
                self._timer = None
