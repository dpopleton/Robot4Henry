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


def test_manual_end_is_idempotent():
    fired = []
    sm = SessionManager(on_session_end=lambda: fired.append(True))
    sm.record_activity()

    assert sm.end_session_manually()
    assert not sm.end_session_manually()
    assert fired == [True]


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


def test_timeout_waits_for_a_turn_in_progress():
    """A slow reply that straddles the timeout doesn't end the session."""
    fired = []
    sm = SessionManager(
        on_session_end=lambda: fired.append(True),
        timeout_seconds=0.3
    )
    sm.record_activity()
    time.sleep(0.2)
    assert sm.begin_turn()
    time.sleep(0.4)  # the turn outlasts the timeout
    assert fired == []
    assert sm.is_active()

    sm.end_turn()  # the clock restarts from the end of the turn
    time.sleep(0.2)
    assert fired == []
    time.sleep(0.3)
    assert fired == [True]
    sm.stop()


def test_begin_turn_reports_a_new_session():
    sm = SessionManager(on_session_end=lambda: None)
    assert not sm.begin_turn()
    sm.end_turn()
    assert sm.begin_turn()
    sm.end_turn()
    sm.stop()
