"""Rest running while a conversation goes on (R-110).

Real SQLite and ChromaDB on throwaway paths, wired the way RobotBrain wires
them (RawLogger and KeyFactsStore on the same database file, each with its
own connection), and a fake LLM. Rest runs in its background thread over
several ended sessions while the main thread holds a conversation.
"""
import threading
import time

from brain.memory.key_facts import KeyFactsStore
from brain.memory.long_term import LongTermMemory
from brain.raw_logger import RawLogger
from brain.rest_process import RestProcess
from tests.brain.fake_embedding import FakeEmbedding

OLD_SESSIONS = 6
CHAT_TURNS = 40


class FakeLLM:
    """Answers each rest prompt by its first words, slowly enough that rest
    and the conversation interleave."""

    def __init__(self, delay=0.002, fail_compress_once=False):
        self.delay = delay
        self.fail_compress_once = fail_compress_once
        self._lock = threading.Lock()

    def complete(self, prompt, options=None):
        time.sleep(self.delay)
        if prompt.startswith("Read only what the USER said"):
            return "pet: cat\nfavourite toy: lego"
        if prompt.startswith("Read this conversation"):
            return "1. Henry has a cat.\n2. Henry likes building with Lego."
        if prompt.startswith("Summarise"):
            with self._lock:
                if self.fail_compress_once:
                    self.fail_compress_once = False
                    raise RuntimeError("killed part-way through rest")
            return "Henry talked about his cat and Lego."
        raise AssertionError(f"unexpected prompt: {prompt[:40]!r}")


def _stores(tmp_path):
    db = str(tmp_path / "robot.db")
    raw_logger = RawLogger(db_path=db)
    key_facts = KeyFactsStore(db_path=db)
    long_term = LongTermMemory(chroma_path=str(tmp_path / "chroma"),
                               embedding_function=FakeEmbedding())
    return raw_logger, key_facts, long_term


def _finished_session(raw_logger) -> str:
    session_id = raw_logger.start_session()
    for line in ("Hi Qbot!", "I have a cat.", "I like lego.", "Bye!"):
        raw_logger.log("user", line)
        raw_logger.log("assistant", "That's great!")
    raw_logger.end_session()
    return session_id


def _processed(raw_logger) -> set:
    with raw_logger._lock:
        rows = raw_logger.conn.execute(
            "SELECT session_id FROM sessions WHERE processed = 1").fetchall()
    return {r[0] for r in rows}


def test_rest_during_a_conversation(tmp_path):
    raw_logger, key_facts, long_term = _stores(tmp_path)
    old = [_finished_session(raw_logger) for _ in range(OLD_SESSIONS)]
    rest = RestProcess(llm=FakeLLM(), raw_logger=raw_logger,
                       long_term=long_term, key_facts=key_facts)

    rest.run()  # background thread, as at the end of a real session
    current = raw_logger.start_session()
    rest_overlapped = False
    for turn in range(CHAT_TURNS):
        # What a turn touches: the log, key facts and long-term memory
        raw_logger.log("user", f"message {turn}")
        key_facts.format_for_prompt()
        long_term.retrieve(f"message {turn} about my cat")
        raw_logger.log("assistant", f"reply {turn}")
        rest_overlapped |= any(t.is_alive() for t in rest._threads)
    rest.wait()

    assert rest_overlapped, "rest finished before the conversation began; test proves nothing"
    # Every old session rested (a failure would have released its claim)
    assert _processed(raw_logger) == set(old)
    # Two memories per session, one set each, with stable ids
    assert long_term.count() == 2 * OLD_SESSIONS
    for session_id in old:
        ids = long_term.collection.get(where={"session_id": session_id})["ids"]
        assert sorted(ids) == [f"{session_id}-0", f"{session_id}-1"]
    assert key_facts.get_all() == {"pet": "cat", "favourite toy": "lego"}
    # The conversation lost nothing and kept its order
    messages = raw_logger.get_session_messages(current)
    assert [m["content"] for m in messages] == [
        text for turn in range(CHAT_TURNS) for text in (f"message {turn}", f"reply {turn}")
    ]
    assert current not in _processed(raw_logger)


def test_two_rests_at_once_rest_each_session_once(tmp_path):
    raw_logger, key_facts, long_term = _stores(tmp_path)
    old = [_finished_session(raw_logger) for _ in range(OLD_SESSIONS)]
    rest = RestProcess(llm=FakeLLM(), raw_logger=raw_logger,
                       long_term=long_term, key_facts=key_facts)

    rest.run()
    rest.run()  # e.g. a timeout ending one session as another ends
    rest.wait()

    assert _processed(raw_logger) == set(old)
    assert long_term.count() == 2 * OLD_SESSIONS


def test_re_resting_after_a_crash_leaves_the_same_memories(tmp_path):
    raw_logger, key_facts, long_term = _stores(tmp_path)
    session_id = _finished_session(raw_logger)

    # First rest stores the memories, then dies before archiving the session
    RestProcess(llm=FakeLLM(fail_compress_once=True), raw_logger=raw_logger,
                long_term=long_term, key_facts=key_facts).run(blocking=True)
    assert session_id not in _processed(raw_logger)
    assert long_term.count() == 2

    # The next start recovers it and rest runs again
    raw_logger.recover_interrupted_sessions()
    RestProcess(llm=FakeLLM(), raw_logger=raw_logger,
                long_term=long_term, key_facts=key_facts).run(blocking=True)

    assert session_id in _processed(raw_logger)
    assert long_term.count() == 2
    assert sorted(long_term.collection.get(where={"session_id": session_id})["documents"]) == [
        "Henry has a cat.", "Henry likes building with Lego."]
