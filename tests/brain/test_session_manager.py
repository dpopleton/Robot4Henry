import pytest
import time
from brain.session_manager import SessionManager


def test_session_starts_inactive():
    sm = SessionManager(on_session_end=lambda: None)
    assert not sm.is_active()
    sm.stop()


def test_activity_marks_active():
    sm = SessionManager(on_session_end=lambda: None)
    sm.record_activity()
    assert sm.is_active()
    sm.stop()


def test_manual_end_fires_callback():
    fired = []
    sm = SessionManager(on_session_end=lambda: fired.append(True))
    sm.record_activity()
    sm.end_session_manually()
    assert len(fired) == 1
    assert not sm.is_active()


def test_timeout_fires_callback():
    fired = []
    sm = SessionManager(
        on_session_end=lambda: fired.append(True),
        timeout_seconds=1
    )
    sm.record_activity()
    time.sleep(1.5)
    assert len(fired) == 1


def test_activity_resets_timer():
    fired = []
    sm = SessionManager(
        on_session_end=lambda: fired.append(True),
        timeout_seconds=1
    )
    sm.record_activity()
    time.sleep(0.7)
    sm.record_activity()  # reset timer
    time.sleep(0.7)

    # Should not have fired yet
    assert len(fired) == 0

    time.sleep(0.5)
    assert len(fired) == 1
    sm.stop()