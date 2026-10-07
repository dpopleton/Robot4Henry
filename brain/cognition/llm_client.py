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

    def complete(self, prompt: str) -> str:
        """Simple single prompt completion."""
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"]

    def complete_json(self, prompt: str) -> dict:
        import json
        import re

        json_prompt = prompt + "\n\nJSON only. No markdown. No extra text."

        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": json_prompt}],
            options={"num_predict": 500}  # enough for JSON, not runaway
        )
        cleaned = response["message"]["content"].strip()

        # Strip markdown fences
        if "```" in cleaned:
            match = re.search(r'```(?:json)?\s*(.*?)```', cleaned, re.DOTALL)
            if match:
                cleaned = match.group(1).strip()

        # Find first complete JSON object
        match = re.search(r'\{.*\}', cleaned, re.DOTALL)
        if match:
            cleaned = match.group(0)

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            print(f"[LLM] JSON parse failed. Raw: {cleaned[:200]}")
            return {}