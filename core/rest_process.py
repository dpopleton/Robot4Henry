import threading
from datetime import datetime
from core.raw_logger import RawLogger
from core.memory.long_term import LongTermMemory
from core.memory.key_facts import KeyFactsStore
from core.llm_client import LLMClient


class RestProcess:
    def __init__(self, llm: LLMClient, raw_logger: RawLogger,
                 long_term: LongTermMemory, key_facts: KeyFactsStore):
        self.llm = llm
        self.raw_logger = raw_logger
        self.long_term = long_term
        self.key_facts = key_facts

    def run(self):
        """Fire and forget — called from session end callback."""
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
            try:
                self._process_session(session_id)
            except Exception as e:
                print(f"[Rest process] Error processing {session_id}: {e}")

        print("[Rest process] Complete.")

    def _process_session(self, session_id: str):
        messages = self.raw_logger.get_session_messages(session_id)

        if not messages:
            return

        formatted = self._format_messages(messages)

        # Step 1 — extract and update key facts
        #Skipping this for now
        #self._extract_key_facts(formatted)

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
    List any personal facts the user directly stated.
    One fact per line. If nothing stated, write NONE.

    USER lines only:
    {user_lines}

    Facts (one per line):"""

        response = self.llm.complete(prompt).strip()
        print(f"[Rest process] Raw facts response: {response}")

        if not response or "NONE" in response.upper():
            return

        # Second pass — verify each candidate against conversation
        candidates = [l.strip() for l in response.split("\n") if l.strip()]
        for candidate in candidates:
            if not self._verify_fact(candidate, conversation):
                print(f"[Rest process] Rejected hallucinated fact: {candidate}")
                continue
            # Parse into key/value
            kv = self._parse_fact_line(candidate)
            if kv:
                key, value = kv
                self.key_facts.set(key, value)
                print(f"[Rest process] Fact stored: {key} = {value}")

    def _user_only(self, conversation: str) -> str:
        """Extract only USER lines from conversation."""
        lines = []
        for line in conversation.split("\n"):
            if line.startswith("USER:"):
                lines.append(line)
        return "\n".join(lines) if lines else conversation

    def _verify_fact(self, fact: str, conversation: str) -> bool:
        """Ask the model to confirm the fact actually appears in the conversation."""
        prompt = f"""Does this conversation contain this fact?
    Answer YES or NO only.

    CONVERSATION:
    {conversation}

    FACT: {fact}

    Answer:"""
        response = self.llm.complete(prompt).strip().upper()
        return response.startswith("YES")

    def _parse_fact_line(self, line: str) -> tuple | None:
        """Parse 'name is Henry' or 'name: Henry' into (key, value)."""
        import re
        # Try "key: value" or "key is value" patterns
        match = re.match(r'^(.+?)(?:\s+is\s+|:\s*)(.+)$', line, re.IGNORECASE)
        if match:
            key = match.group(1).strip().lower()
            value = match.group(2).strip()
            # Skip if value looks hallucinated
            if value.lower() in ("unknown", "none", "not mentioned", "no one", "n/a"):
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

        return self.llm.complete(prompt)
