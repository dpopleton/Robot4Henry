import threading
from datetime import datetime
from brain.raw_logger import RawLogger
from brain.memory.long_term import LongTermMemory
from brain.memory.key_facts import KeyFactsStore
from brain.cognition.llm_client import LLMClient


class RestProcess:
    def __init__(self, llm: LLMClient, raw_logger: RawLogger,
                 long_term: LongTermMemory, key_facts: KeyFactsStore):
        self.llm = llm
        self.raw_logger = raw_logger
        self.long_term = long_term
        self.key_facts = key_facts

    def run(self, blocking: bool = False):
        """Fire and forget by default (called from session end callback).
        blocking=True runs it inline and returns once done — used by
        scenario tests/tools that need to inspect long term memory right after."""
        if blocking:
            self._process()
            return
        thread = threading.Thread(target=self._process, daemon=True)
        thread.start()

    def _process(self):
        """Process all unprocessed sessions into long term memory."""
        sessions = self.raw_logger.get_unprocessed_sessions()

        if not sessions:
            print("[Rest process] No sessions to process.")
            return

        print(f"[Rest process] Processing {len(sessions)} session(s)...")

        for session_id in sessions:
            if not self.raw_logger.claim_session_for_processing(session_id):
                continue
            try:
                self._process_session(session_id)
            except Exception as e:
                self.raw_logger.release_processing_claim(session_id)
                print(f"[Rest process] Error processing {session_id}: {e}")

        print("[Rest process] Complete.")

    def _process_session(self, session_id: str):
        messages = self.raw_logger.get_session_messages(session_id)

        if not messages:
            self.raw_logger.mark_processed(session_id, "")
            return

        formatted = self._format_messages(messages)

        # Step 1 — extract and update key facts.  This belongs in rest rather
        # than the turn path: it has no effect on reply latency and works from
        # the complete, durable transcript once a session has ended.
        self._extract_key_facts(formatted)

        # Step 2 — build long term memory chunks
        self._build_long_term_memories(formatted, session_id)

        # Step 3 — compress and archive raw log
        compressed = self._compress(formatted)
        self.raw_logger.mark_processed(session_id, compressed)

        print(f"[Rest process] Session {session_id[:8]}... archived.")

    def _format_messages(self, messages: list) -> str:
        lines = []
        for m in messages:
            role = m["role"].upper()
            lines.append(f"{role}: {m['content']}")
        return "\n".join(lines)

    def _extract_key_facts(self, conversation: str):
        user_lines = self._user_only(conversation)
        print(f"[Rest process] User lines:\n{user_lines}")

        prompt = f"""Read only what the USER said in this conversation.
    List stable personal facts the user directly stated, such as their name,
    age, pets, favourites or important preferences. Do not infer anything and
    do not repeat questions or facts said by the assistant.
    Write each fact as a concise `key: value` line (for example, `name: Henry`
    or `favourite animal: dinosaur`). If nothing qualifies, write NONE.

    USER lines only:
    {user_lines}

    Facts (one per line):"""

        # Temperature 0: the 1B model otherwise sometimes answers a bare NONE
        # for a conversation that plainly contains facts.
        response = self.llm.complete(prompt, options={"temperature": 0}).strip()
        print(f"[Rest process] Raw facts response: {response}")

        # Judge each line on its own.  The model pads its list with lines
        # like `pets: NONE` and invented favourites, so a NONE anywhere must
        # not throw away the real facts beside it.
        for candidate in (l.strip() for l in response.split("\n")):
            kv = self._parse_fact_line(candidate)
            if not kv:
                continue
            key, value = kv
            if not self._is_grounded(value, user_lines):
                print(f"[Rest process] Rejected hallucinated fact: {candidate}")
                continue
            self.key_facts.set(key, value)
            print(f"[Rest process] Fact stored: {key} = {value}")

    def _user_only(self, conversation: str) -> str:
        """Extract only USER lines from conversation."""
        lines = []
        for line in conversation.split("\n"):
            if line.startswith("USER:"):
                lines.append(line)
        return "\n".join(lines) if lines else conversation

    @staticmethod
    def _is_grounded(value: str, user_lines: str) -> bool:
        """True if every word of the fact's value appears in what the user
        said (ignoring a plural "s"). A plain check rather than asking the
        model "is this true?" — on a 1B model that question is close to a
        coin flip, while invented values (sushi, age 30) never appear in the
        user's own words. See D-011."""
        import re
        def words(text):
            return {w.removesuffix("s") for w in re.findall(r"[a-z0-9']+", text.lower())}
        value_words = words(value)
        return bool(value_words) and value_words <= words(user_lines)

    def _parse_fact_line(self, line: str) -> tuple | None:
        """Parse a concise ``key: value`` or ``key is value`` fact line."""
        import re
        line = re.sub(r'^(?:[-*]|\d+[.)])\s*', '', line.strip())
        # Try "key: value" or "key is value" patterns
        match = re.match(r'^(.+?)(?:\s+is\s+|:\s*)(.+)$', line, re.IGNORECASE)
        if match:
            key = match.group(1).strip().lower()
            value = match.group(2).strip()
            # Skip if value looks hallucinated
            if not value or value.lower() in ("unknown", "none", "not mentioned", "no one", "n/a"):
                return None
            if len(key) > 30 or len(value) > 100:
                return None
            return (key, value)
        return None

    def _build_long_term_memories(self, conversation: str, session_id: str):
        lines = [l for l in conversation.split("\n") if l.strip()]
        if len(lines) < 4:
            return

        prompt = f"""Read this conversation and list up to 5 memorable facts.
    Include things both the user and assistant said that are worth remembering.
    Write one fact per line as a complete sentence.
    If nothing is memorable, write NONE.

    CONVERSATION:
    {conversation}

    Facts (one per line):"""

        response = self.llm.complete(prompt).strip()

        if not response or "NONE" in response.upper():
            return

        # Parse plain text lines into memories
        memories = self._parse_memory_lines(response)

        for memory in memories:
            self.long_term.store(
                memory,
                metadata={
                    "session_id": session_id,
                    "created_at": datetime.now().isoformat()
                }
            )
            print(f"[Rest process] Memory stored: {memory}")

    def _parse_memory_lines(self, response: str) -> list:
        import re
        # Phrases that indicate intro/preamble lines
        skip_patterns = [
            r'^here are',
            r'^the following',
            r'^these are',
            r'^below are',
            r'^facts from',
            r'^memorable',
        ]

        memories = []
        for line in response.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Strip numbering
            line = re.sub(r'^[\d\-\*\.\)]+\s*', '', line).strip()
            if len(line) < 10:
                continue
            if line.upper() == "NONE":
                continue
            # Skip preamble lines
            lower = line.lower()
            if any(re.match(p, lower) for p in skip_patterns):
                continue
            # Skip lines ending with colon (introductory lines)
            if line.endswith(":"):
                continue
            memories.append(line)

        return memories[:5]

    def _compress(self, conversation: str) -> str:
        prompt = f"""Summarise this conversation in 2-3 sentences.
    Keep only the most important facts.

    CONVERSATION:
    {conversation}

    Summary:"""
        return self.llm.complete(prompt).strip()
