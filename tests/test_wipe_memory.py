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
