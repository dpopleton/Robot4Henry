from brain.cognition.robot_brain import RobotBrain
import time
from unittest.mock import MagicMock


class FactExtractingLLM:
    """Small deterministic stand-in for the rest-process LLM calls."""
    def __init__(self):
        self.system_prompts = []

    def chat(self, system_prompt, messages, format=None):
        self.system_prompts.append(system_prompt)
        return '{"reply": "Hello!", "mood": {"category": "happy", "intensity": 1}}'

    def complete(self, prompt, options=None):
        if "Facts (one per line):" in prompt:
            return "name: Henry"
        if "Summary:" in prompt:
            return "Henry introduced himself."
        raise AssertionError(f"Unexpected completion prompt: {prompt}")


def test_llm_failure_is_a_logged_retryable_exchange(tmp_path):
    brain = RobotBrain(
        db_path=str(tmp_path / "robot.db"),
        chroma_path=str(tmp_path / "chroma"),
    )
    brain.llm.chat = lambda *args, **kwargs: (_ for _ in ()).throw(ConnectionError("offline"))

    reply = brain.chat("Hello")

    assert "trouble thinking" in reply
    assert brain.session.is_active()
    messages = brain.raw_logger.get_session_messages(brain.raw_logger.current_session_id)
    assert [(message["role"], message["content"]) for message in messages] == [
        ("user", "Hello"),
        ("assistant", reply),
    ]
    brain.session.stop()
    brain.raw_logger.conn.close()


def test_end_session_is_idempotent(tmp_path):
    brain = RobotBrain(
        db_path=str(tmp_path / "robot.db"),
        chroma_path=str(tmp_path / "chroma"),
    )
    brain.llm.chat = MagicMock(return_value='{"reply": "Hello!", "mood": {"category": "happy", "intensity": 1}}')
    brain.rest_process.run = MagicMock()
    brain.chat("Hello")

    brain.end_session()
    brain.end_session()

    assert not brain.session.is_active()
    assert brain.raw_logger.current_session_id is None
    brain.rest_process.run.assert_called_once_with(blocking=False)
    brain.raw_logger.conn.close()


def test_key_fact_survives_restart_and_is_added_to_later_prompt(tmp_path):
    """A completed session writes a fact that a fresh brain process receives."""
    db_path = str(tmp_path / "robot.db")
    chroma_path = str(tmp_path / "chroma")
    first_brain = RobotBrain(db_path=db_path, chroma_path=chroma_path)
    first_brain.llm = FactExtractingLLM()
    first_brain.rest_process.llm = first_brain.llm

    first_brain.chat("My name is Henry.")
    first_brain.force_rest(blocking=True)
    assert first_brain.key_facts.get("name") == "Henry"

    restarted_brain = RobotBrain(db_path=db_path, chroma_path=chroma_path)
    restarted_llm = FactExtractingLLM()
    restarted_brain.llm = restarted_llm
    restarted_brain.chat("What should we play?")

    assert "KEY FACTS ABOUT THE USER:\n  - name: Henry" in restarted_llm.system_prompts[-1]

    for brain in (first_brain, restarted_brain):
        brain.session.stop()
        brain.raw_logger.conn.close()
        brain.key_facts.conn.close()


def test_timeout_during_a_slow_reply_keeps_the_turn_in_one_session(tmp_path):
    """The reply to a message sent just before the timeout belongs to the
    same session as the message, and the timeout doesn't fire mid-turn."""
    brain = RobotBrain(
        db_path=str(tmp_path / "robot.db"),
        chroma_path=str(tmp_path / "chroma"),
    )
    brain.session._timeout_seconds = 0.3
    brain.rest_process.run = MagicMock()

    def slow_chat(*args, **kwargs):
        time.sleep(0.5)  # longer than the timeout
        return '{"reply": "Hello!", "mood": {"category": "happy", "intensity": 1}}'
    brain.llm.chat = slow_chat

    brain.chat("Hello")
    session_id = brain.raw_logger.current_session_id
    messages = brain.raw_logger.get_session_messages(session_id)
    assert [m["role"] for m in messages] == ["user", "assistant"]
    assert brain.session.is_active()
    brain.rest_process.run.assert_not_called()

    time.sleep(0.5)  # now idle past the timeout
    assert not brain.session.is_active()
    brain.rest_process.run.assert_called_once_with(blocking=False)
    brain.raw_logger.conn.close()


def _fact_brain(tmp_path):
    brain = RobotBrain(
        db_path=str(tmp_path / "robot.db"),
        chroma_path=str(tmp_path / "chroma"),
    )
    brain.llm = FactExtractingLLM()
    brain.rest_process.llm = brain.llm
    return brain


def _slow_rest(brain):
    """Make rest take a moment, as it does on the robot laptop."""
    process = brain.rest_process._process
    brain.rest_process._process = lambda: (time.sleep(0.3), process())


def test_shutdown_rests_the_last_session_before_returning(tmp_path):
    """Quitting straight after a conversation still stores its key facts."""
    brain = _fact_brain(tmp_path)
    _slow_rest(brain)
    brain.chat("My name is Henry.")

    brain.shutdown()

    assert brain.key_facts.get("name") == "Henry"
    brain.raw_logger.conn.close()
    brain.key_facts.conn.close()


def test_shutdown_waits_for_a_rest_already_running(tmp_path):
    """A timeout's background rest isn't killed by quitting."""
    brain = _fact_brain(tmp_path)
    _slow_rest(brain)
    brain.chat("My name is Henry.")
    brain.end_session()  # background rest, like the timeout path

    brain.shutdown()

    assert brain.key_facts.get("name") == "Henry"
    brain.raw_logger.conn.close()
    brain.key_facts.conn.close()


def test_startup_recovers_a_session_cut_off_by_a_crash(tmp_path):
    db_path = str(tmp_path / "robot.db")
    chroma_path = str(tmp_path / "chroma")
    crashed = RobotBrain(db_path=db_path, chroma_path=chroma_path)
    crashed.llm = FactExtractingLLM()
    crashed.chat("My name is Henry.")
    crashed.session.stop()  # power cut: no shutdown, no rest

    restarted = RobotBrain(db_path=db_path, chroma_path=chroma_path)
    restarted.llm = FactExtractingLLM()
    restarted.rest_process.llm = restarted.llm
    restarted.force_rest(blocking=True)

    assert restarted.key_facts.get("name") == "Henry"
    for brain in (crashed, restarted):
        brain.raw_logger.conn.close()
        brain.key_facts.conn.close()
