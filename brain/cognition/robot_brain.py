import threading
from brain.cognition.llm_client import LLMClient
from brain.memory.short_term import ShortTermMemory
from brain.memory.medium_term import MediumTermMemory
from brain.memory.key_facts import KeyFactsStore
from brain.memory.long_term import LongTermMemory
from brain.raw_logger import RawLogger
from brain.session_manager import SessionManager
from brain.rest_process import RestProcess
from brain.limbic import LimbicSystem, CATEGORIES
from brain.cognition.response_schema import CHAT_RESPONSE_SCHEMA, parse_chat_response
from config.settings import PRIMARY_MODEL, DB_PATH, CHROMA_PATH


class RobotBrain:
    def __init__(self, db_path: str = DB_PATH, chroma_path: str = CHROMA_PATH):
        """db_path/chroma_path are overridable so tests and tools can point
        a brain at isolated, disposable storage instead of the real thing."""
        self.llm = LLMClient(model=PRIMARY_MODEL)

        # Memory layers
        self.short_term = ShortTermMemory()
        self.medium_term = MediumTermMemory(self.llm)
        self.key_facts = KeyFactsStore(db_path=db_path)
        self.long_term = LongTermMemory(chroma_path=chroma_path)

        # Mood
        self.limbic = LimbicSystem()

        # Logging and session management
        self.raw_logger = RawLogger(db_path=db_path)
        recovered = self.raw_logger.recover_interrupted_sessions()
        if recovered:
            print(f"[Recovered {recovered} interrupted session(s) for the next rest]")
        # Turns and session endings take this lock so the timeout thread
        # never ends a session underneath a turn.
        self._turn_lock = threading.RLock()
        self.session = SessionManager(
            on_session_end=self._handle_session_end
        )

        # Rest process
        self.rest_process = RestProcess(
            llm=self.llm,
            raw_logger=self.raw_logger,
            long_term=self.long_term,
            key_facts=self.key_facts
        )

    def chat(self, user_input: str) -> str:
        with self._turn_lock:
            # begin_turn() holds off the inactivity timeout until the turn
            # ends, however slow the reply.
            was_active = self.session.begin_turn()
            try:
                if not was_active:
                    # Rest any session a timeout ended before its own
                    # clean-up got the lock, so it isn't mixed into this one.
                    if self.raw_logger.current_session_id:
                        self._rest(blocking=False)
                    self.raw_logger.start_session()
                    self.limbic.wake()
                return self._turn(user_input)
            finally:
                self.session.end_turn()

    def _turn(self, user_input: str) -> str:
        # Log raw input immediately
        self.raw_logger.log("user", user_input)

        # Build system prompt
        system_prompt = self._build_system_prompt(user_input)

        # Assemble messages for LLM
        messages = self.short_term.get_messages() + [
            {"role": "user", "content": user_input}
        ]

        # Get response — format=CHAT_RESPONSE_SCHEMA constrains the model
        # to a {"reply": ..., "mood": {...}} shape rather than hoping it
        # remembers to append a free-text tag.
        try:
            raw_response = self.llm.chat(system_prompt, messages, format=CHAT_RESPONSE_SCHEMA)
        except Exception as error:
            # The robot remains usable if Ollama is restarting or unavailable.
            # Record the failure as a normal, reviewable exchange rather than
            # leaving the session half-open.
            print(f"[LLM] Chat failed: {error}")
            response = "I'm having trouble thinking right now. Please try me again in a moment."
            self.raw_logger.log("assistant", response)
            self.short_term.add("user", user_input)
            self.short_term.add("assistant", response)
            return response

        # A missing/malformed mood object just means no mood update this
        # turn; a broken `reply` falls back to the raw text (see
        # parse_chat_response) so a structure slip never costs an answer.
        response, mood_signal = parse_chat_response(raw_response)
        if mood_signal:
            self.limbic.react(*mood_signal)

        # Log raw response
        self.raw_logger.log("assistant", response)

        # Update short term — evict oldest if overflow
        self.short_term.add("user", user_input)
        evicted = self.short_term.add("assistant", response)

        # Compress evicted exchange into medium term
        if evicted:
            self.medium_term.update(evicted)

        return response

    def _build_system_prompt(self, current_input: str) -> str:
        relevant_memories = self.long_term.retrieve(current_input)

        sections = [
            self._personality(),
            self._mood_context(),
            self._response_format(),
            self.key_facts.format_for_prompt(),
            self._format_long_term(relevant_memories),
            self.medium_term.format_for_prompt(),
        ]

        return "\n\n".join(s for s in sections if s.strip())

    def _personality(self) -> str:
        return """/no_think
You are Qbot, a friendly and playful robot companion for a young child.
You are warm, encouraging, and speak simply and clearly.
You are curious and love to learn alongside the child.
You never say anything scary, mean, or inappropriate.
If you are ever unsure whether something is suitable,
you say you need to check with a grown-up first."""

    def _mood_context(self) -> str:
        mood = self.limbic.current
        return f"""YOUR CURRENT MOOD: you are feeling {mood.describe()} right now.
Let this mood colour your tone naturally — don't announce it outright."""

    def _response_format(self) -> str:
        return f"""Respond with a JSON object with exactly two fields:
  "reply": your spoken reply to the child, as plain text.
  "mood": how this exchange made you feel, as {{"category": ..., "intensity": ...}}
    categories: {", ".join(CATEGORIES)}
    intensity: 1 (a little), 2 (quite), 3 (very)"""

    def _format_long_term(self, memories: list) -> str:
        if not memories:
            return ""
        lines = [f"  - {m}" for m in memories]
        return "RELEVANT MEMORIES:\n" + "\n".join(lines)

    def _handle_session_end(self):
        """Inactivity timeout, on the timer thread."""
        with self._turn_lock:
            # A turn that started after the timeout fired has already
            # rested the old session and opened a new one.
            if self.session.is_active():
                return
            print("[Session ended — clearing short and medium term memory]")
            self._rest(blocking=False)

    def _rest(self, blocking: bool):
        self.raw_logger.end_session()
        self.rest_process.run(blocking=blocking)

        # Clear in-session memory
        self.medium_term.clear()
        self.short_term.clear()

    def force_rest(self, blocking: bool = False):
        """End the session and run the rest process now. blocking=True waits
        for long term memory to actually be written before returning —
        used by scenario tests/tools, not the real inactivity-timeout path."""
        with self._turn_lock:
            self.session.end_session_manually(notify=False)
            self._rest(blocking=blocking)

    def end_session(self, blocking: bool = False):
        """Public, idempotent session end used by the terminal UI."""
        with self._turn_lock:
            if self.session.end_session_manually(notify=False):
                self._rest(blocking=blocking)

    def shutdown(self):
        """Rest the last session and wait for any rest still running, so
        quitting never loses the final conversation's memories."""
        self.session.stop()
        print("[Resting before shutdown...]")
        self.end_session(blocking=True)
        self.rest_process.wait()
