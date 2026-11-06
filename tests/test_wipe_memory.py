import sys

import config.settings as settings
import wipe_memory
from brain.memory.key_facts import KeyFactsStore
from brain.raw_logger import RawLogger


def test_default_wipe_keeps_reviewable_raw_logs(tmp_path, monkeypatch):
    db_path = tmp_path / "robot.db"
    chroma_path = tmp_path / "chroma"
    monkeypatch.setattr(settings, "DB_PATH", str(db_path))
    monkeypatch.setattr(settings, "CHROMA_PATH", str(chroma_path))

    logger = RawLogger(str(db_path))
    logger.log("user", "Please remember this.")
    session_id = logger.current_session_id
    logger.end_session()
    logger.conn.close()
    facts = KeyFactsStore(str(db_path))
    facts.set("name", "Henry")
    facts.conn.close()

    monkeypatch.setattr(sys, "argv", ["wipe_memory.py"])
    wipe_memory.main()

    check = RawLogger(str(db_path))
    assert check.get_session_messages(session_id)[0]["content"] == "Please remember this."
    facts = KeyFactsStore(str(db_path))
    assert facts.get("name") is None
    facts.conn.close()
    check.conn.close()


def test_wipe_all_clears_raw_logs_too(tmp_path, monkeypatch):
    db_path = tmp_path / "robot.db"
    chroma_path = tmp_path / "chroma"
    monkeypatch.setattr(settings, "DB_PATH", str(db_path))
    monkeypatch.setattr(settings, "CHROMA_PATH", str(chroma_path))

    with RawLogger(str(db_path)) as logger:
        logger.log("user", "Secret")
        session_id = logger.current_session_id
        logger.end_session()
    with KeyFactsStore(str(db_path)) as facts:
        facts.set("name", "Henry")

    monkeypatch.setattr(sys, "argv", ["wipe_memory.py", "--all"])
    wipe_memory.main()

    with RawLogger(str(db_path)) as check:
        assert check.get_session_messages(session_id) == []
    with KeyFactsStore(str(db_path)) as facts:
        assert facts.get("name") is None


def test_wipe_facts_only_preserves_logs(tmp_path, monkeypatch):
    db_path = tmp_path / "robot.db"
    chroma_path = tmp_path / "chroma"
    monkeypatch.setattr(settings, "DB_PATH", str(db_path))
    monkeypatch.setattr(settings, "CHROMA_PATH", str(chroma_path))

    with RawLogger(str(db_path)) as logger:
        logger.log("user", "Keep log")
        session_id = logger.current_session_id
        logger.end_session()
    with KeyFactsStore(str(db_path)) as facts:
        facts.set("name", "Henry")

    monkeypatch.setattr(sys, "argv", ["wipe_memory.py", "--facts-only"])
    wipe_memory.main()

    with RawLogger(str(db_path)) as check:
        assert len(check.get_session_messages(session_id)) == 1
    with KeyFactsStore(str(db_path)) as facts:
        assert facts.get("name") is None


def test_wipe_dry_run_leaves_everything_intact(tmp_path, monkeypatch):
    db_path = tmp_path / "robot.db"
    chroma_path = tmp_path / "chroma"
    monkeypatch.setattr(settings, "DB_PATH", str(db_path))
    monkeypatch.setattr(settings, "CHROMA_PATH", str(chroma_path))

    with RawLogger(str(db_path)) as logger:
        logger.log("user", "Untouched")
        session_id = logger.current_session_id
        logger.end_session()
    with KeyFactsStore(str(db_path)) as facts:
        facts.set("name", "Henry")

    monkeypatch.setattr(sys, "argv", ["wipe_memory.py", "--all", "--dry-run"])
    wipe_memory.main()

    with RawLogger(str(db_path)) as check:
        assert len(check.get_session_messages(session_id)) == 1
    with KeyFactsStore(str(db_path)) as facts:
        assert facts.get("name") == "Henry"


def test_wipe_handles_nonexistent_paths_without_error(tmp_path, monkeypatch):
    db_path = tmp_path / "nonexistent" / "robot.db"
    chroma_path = tmp_path / "nonexistent" / "chroma"
    monkeypatch.setattr(settings, "DB_PATH", str(db_path))
    monkeypatch.setattr(settings, "CHROMA_PATH", str(chroma_path))

    monkeypatch.setattr(sys, "argv", ["wipe_memory.py", "--all"])
    wipe_memory.main()  # Should not raise any exceptions

