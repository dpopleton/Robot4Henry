"""
The shape of a chat turn's response. Used to ask Ollama for structured
output (a JSON schema) instead of hoping the model remembers to append a
free-text 'MOOD: category:intensity' line — small models are unreliable
at the latter but can be constrained to the former at decode time.

Currently just `reply` + `mood`, but this is the natural place to grow
more fields later (e.g. params for other organs/subroutines) without
re-inventing a text-tag convention for each one.
"""
import json

from brain.limbic.mood import CATEGORIES, MIN_INTENSITY, MAX_INTENSITY

CHAT_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "reply": {
            "type": "string",
            "minLength": 1,
        },
        "mood": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": list(CATEGORIES)},
                "intensity": {"type": "integer", "minimum": MIN_INTENSITY, "maximum": MAX_INTENSITY},
            },
            "required": ["category", "intensity"],
        },
    },
    "required": ["reply", "mood"],
}


def parse_chat_response(raw: str) -> tuple[str, tuple[str, int] | None]:
    """
    Parse a {"reply": ..., "mood": {"category": ..., "intensity": ...}}
    response. Returns (reply_text, (category, intensity) | None).

    A malformed/incomplete response (bad JSON, missing field, invalid
    category/intensity) just means no mood update this turn, same
    philosophy the old free-text tag parsing had — and we still fall
    back to the raw text as the reply, so a broken `mood` object never
    costs the user an answer.
    """
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return raw.strip(), None

    if not isinstance(data, dict):
        return raw.strip(), None

    reply = data.get("reply")
    if not isinstance(reply, str) or not reply.strip():
        return raw.strip(), None
    reply = reply.strip()

    return reply, _parse_mood(data.get("mood"))


def _parse_mood(mood) -> tuple[str, int] | None:
    if not isinstance(mood, dict):
        return None

    category = mood.get("category")
    intensity = mood.get("intensity")

    if not isinstance(category, str) or category.lower() not in CATEGORIES:
        return None
    if isinstance(intensity, bool) or not isinstance(intensity, int):
        return None
    if not (MIN_INTENSITY <= intensity <= MAX_INTENSITY):
        return None

    return category.lower(), intensity
