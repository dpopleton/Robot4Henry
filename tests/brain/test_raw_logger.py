import tempfile
import pytest
import os
from brain.raw_logger import RawLogger

TEST_DB = "storage/test_raw.db"


@pytest.fixture
def logger():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    l = RawLogger(db_path=db_path)
    yield l
    l.conn.close()
    os.remove(db_path)


def test_start_session(logger):
    session_id = logger.start_session()
    assert session_id is not None
    assert logger.current_session_id == session_id


def test_log_creates_messages(logger):
    logger.start_session()
    logger.log("user", "Hello")
    logger.log("assistant", "Hi there")

    messages = logger.get_session_messages(logger.current_session_id)
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_auto_starts_session_if_needed(logger):
    assert logger.current_session_id is None
    logger.log("user", "Hello")
    assert logger.current_session_id is not None


def test_end_session(logger):
    logger.start_session()
    logger.log("user", "Hello")
    logger.log("assistant", "Hi")
    session_id = logger.current_session_id
    logger.end_session()

    assert logger.current_session_id is None

    unprocessed = logger.get_unprocessed_sessions()
    assert session_id in unprocessed


def test_mark_processed(logger):
    logger.start_session()
    logger.log("user", "Hello")
    logger.log("assistant", "Hi")
    session_id = logger.current_session_id
    logger.end_session()

    logger.mark_processed(session_id, "Compressed: brief hello exchange.")

    unprocessed = logger.get_unprocessed_sessions()
    assert session_id not in unprocessed

    # Raw messages stay available for the weekly supervised-log review.
    messages = logger.get_session_messages(session_id)
    assert [message["content"] for message in messages] == ["Hello", "Hi"]


def test_only_one_worker_can_claim_a_session(logger):
    logger.start_session()
    logger.log("user", "Hello")
    session_id = logger.current_session_id
    logger.end_session()

    assert logger.claim_session_for_processing(session_id)
    assert not logger.claim_session_for_processing(session_id)
    logger.release_processing_claim(session_id)
    assert logger.claim_session_for_processing(session_id)


def test_session_manager_integration(logger):
    # Simulate two complete sessions
    logger.start_session()
    logger.log("user", "Session 1 message")
    logger.log("assistant", "Session 1 response")
    logger.end_session()

    logger.start_session()
    logger.log("user", "Session 2 message")
    logger.log("assistant", "Session 2 response")
    logger.end_session()

    unprocessed = logger.get_unprocessed_sessions()
    assert len(unprocessed) == 2


def test_recover_interrupted_sessions(logger):
    # Cut off mid-conversation: never ended.
    unended = logger.start_session()
    logger.log("user", "Hello")
    # Cut off mid-rest: claimed but never marked processed.
    claimed = logger.start_session()
    logger.end_session()
    assert logger.claim_session_for_processing(claimed)
    logger.current_session_id = None

    assert logger.get_unprocessed_sessions() == []
    assert logger.recover_interrupted_sessions() == 2
    assert set(logger.get_unprocessed_sessions()) == {unended, claimed}
