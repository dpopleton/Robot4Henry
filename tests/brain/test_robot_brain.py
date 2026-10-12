from brain.cognition.robot_brain import RobotBrain
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
