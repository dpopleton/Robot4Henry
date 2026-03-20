from collections import deque
from config.settings import SHORT_TERM_MAX_EXCHANGES


class ShortTermMemory:
    def __init__(self, max_exchanges: int = SHORT_TERM_MAX_EXCHANGES):
        self.max_exchanges = max_exchanges
        self._messages = []

    def add(self, role: str, content: str) -> list | None:
        """
        Add a message. If adding this exchange causes overflow,
        return the oldest exchange for medium term compression.
        Otherwise return None.
        """
        self._messages.append({"role": role, "content": content})

        # Only check on assistant messages — a complete exchange
        if role == "assistant":
            exchange_count = len(self._messages) // 2
            if exchange_count > self.max_exchanges:
                # Pull oldest exchange off the front
                evicted = self._messages[:2]
                self._messages = self._messages[2:]
                return evicted

        return None

    def get_messages(self) -> list:
        """Return all verbatim messages for LLM context."""
        return list(self._messages)

    def clear(self):
        """Called at session end."""
        self._messages = []

    def exchange_count(self) -> int:
        return len(self._messages) // 2

    def __len__(self):
        return len(self._messages)