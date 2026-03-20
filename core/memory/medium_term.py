class MediumTermMemory:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.summary = ""

    def update(self, evicted_messages: list):
        """
        Absorb evicted exchanges into rolling summary.
        Called during conversation when short term overflows.
        """
        if not evicted_messages:
            return

        formatted = "\n".join(
            f"{m['role'].upper()}: {m['content']}"
            for m in evicted_messages
        )

        if not self.summary:
            prompt = f"""Summarise this conversation excerpt concisely.
Preserve names, key facts, emotional tone, and important details.
Keep it under 150 words.

CONVERSATION:
{formatted}"""
        else:
            prompt = f"""Update this existing summary by incorporating
the new exchanges. Preserve all important details and facts.
Keep the total under 150 words.

EXISTING SUMMARY:
{self.summary}

NEW EXCHANGES:
{formatted}"""

        self.summary = self.llm.complete(prompt)

    def get(self) -> str:
        return self.summary

    def format_for_prompt(self) -> str:
        if not self.summary:
            return ""
        return f"EARLIER IN THIS CONVERSATION:\n{self.summary}"

    def clear(self):
        """Called at session end — medium term is wiped completely."""
        self.summary = ""

    def has_content(self) -> bool:
        return bool(self.summary)