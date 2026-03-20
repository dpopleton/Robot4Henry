from core.llm_client import LLMClient
from core.memory.short_term import ShortTermMemory
from core.memory.medium_term import MediumTermMemory
from core.memory.key_facts import KeyFactsStore
from core.memory.long_term import LongTermMemory
from core.raw_logger import RawLogger
from core.session_manager import SessionManager
from core.rest_process import RestProcess
from config.settings import PRIMARY_MODEL


class RobotBrain:
    def __init__(self):
        self.llm = LLMClient(model=PRIMARY_MODEL)

        # Memory layers
        self.short_term = ShortTermMemory()
        self.medium_term = MediumTermMemory(self.llm)
        self.key_facts = KeyFactsStore()
        self.long_term = LongTermMemory()

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

        # Log raw input immediately
        self.raw_logger.log("user", user_input)

        # Build system prompt
        system_prompt = self._build_system_prompt(user_input)

        # Assemble messages for LLM
        messages = self.short_term.get_messages() + [
            {"role": "user", "content": user_input}
        ]

        # Get response
        response = self.llm.chat(system_prompt, messages)

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