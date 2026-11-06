import ollama
from config.settings import PRIMARY_MODEL, OLLAMA_HOST


class LLMClient:
    def __init__(self, model: str = PRIMARY_MODEL):
        self.model = model
        self.client = ollama.Client(host=OLLAMA_HOST)

    def chat(self, system_prompt: str, messages: list, format: dict | str | None = None) -> str:
        """Send a conversation with system prompt, return response text.

        `format` is passed straight through to Ollama — a JSON-schema dict
        constrains the model to emit exactly that shape (see
        brain/cognition/response_schema.py), rather than relying on it
        reliably following a free-text instruction. Omit for plain text.
        """
        full_messages = [
            {"role": "system", "content": system_prompt}
        ] + messages

        response = self.client.chat(
            model=self.model,
            messages=full_messages,
            format=format,
        )
        return response["message"]["content"]

    def complete(self, prompt: str, options: dict | None = None) -> str:
        """Simple single prompt completion. `options` passes Ollama model
        options through (e.g. {"temperature": 0} for repeatable extraction)."""
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            options=options,
        )
        return response["message"]["content"]
