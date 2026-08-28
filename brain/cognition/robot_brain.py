from brain.cognition.llm_client import LLMClient
from brain.memory.short_term import ShortTermMemory
from brain.memory.medium_term import MediumTermMemory
from brain.memory.key_facts import KeyFactsStore
from brain.memory.long_term import LongTermMemory
from brain.raw_logger import RawLogger
from brain.session_manager import SessionManager
from brain.rest_process import RestProcess
from brain.limbic import LimbicSystem, CATEGORIES
from brain.limbic.parsing import extract_mood_tag
from config.settings import PRIMARY_MODEL


class RobotBrain:
    def __init__(self):
        self.llm = LLMClient(model=PRIMARY_MODEL)

        # Memory layers
        self.short_term = ShortTermMemory()
        self.medium_term = MediumTermMemory(self.llm)
        self.key_facts = KeyFactsStore()
        self.long_term = LongTermMemory()

        # Mood
        self.limbic = LimbicSystem()

        # Logging and session management
        self.raw_logger = RawLogger()
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
        # Ensure session is active
        if not self.session.is_active():
            self.raw_logger.start_session()
            self.limbic.wake()

        # Log raw input immediately
        self.raw_logger.log("user", user_input)

        # Build system prompt
        system_prompt = self._build_system_prompt(user_input)

        # Assemble messages for LLM
        messages = self.short_term.get_messages() + [
            {"role": "user", "content": user_input}
        ]

        # Get response
        raw_response = self.llm.chat(system_prompt, messages)

        # Pull the trailing mood tag out before this touches logs, memory,
        # or the user — a missing/malformed tag just means no mood update.
        response, mood_signal = extract_mood_tag(raw_response)
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

        # Record activity — resets inactivity timer
        self.session.record_activity()

        return response

    def _build_system_prompt(self, current_input: str) -> str:
        relevant_memories = self.long_term.retrieve(current_input)

        sections = [
            self._personality(),
            self._mood_context(),
            # Maybe add this later. Doesn't work right now and is being a pain with little in return.
            # self.key_facts.format_for_prompt(),
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
Let this mood colour your tone naturally — don't announce it outright.

At the very end of your reply, on its own new line, add exactly one tag
showing how this exchange made you feel, in this exact format:
MOOD: <category>:<intensity>
categories: {", ".join(CATEGORIES)}
intensity: 1 (a little), 2 (quite), 3 (very)
Example: MOOD: curious:2"""

    def _format_long_term(self, memories: list) -> str:
        if not memories:
            return ""
        lines = [f"  - {m}" for m in memories]
        return "RELEVANT MEMORIES:\n" + "\n".join(lines)

    def _handle_session_end(self):
        print("[Session ended — clearing short and medium term memory]")

        # Trigger rest process first — needs the session marked ended
        self.raw_logger.end_session()
        self.rest_process.run()

        # Clear in-session memory
        self.medium_term.clear()
        self.short_term.clear()

    def shutdown(self):
        self.session.end_session_manually()
        self.session.stop()