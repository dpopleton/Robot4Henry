import re

from brain.limbic.mood import CATEGORIES, MIN_INTENSITY, MAX_INTENSITY

_MOOD_TAG_RE = re.compile(
    r"(?im)^\s*MOOD:\s*(\w+)\s*:\s*([" + str(MIN_INTENSITY) + "-" + str(MAX_INTENSITY) + r"])\s*$"
)


def extract_mood_tag(text: str) -> tuple[str, tuple[str, int] | None]:
    """
    Pull a trailing 'MOOD: <category>:<intensity>' line out of an LLM
    response. Returns (text_with_tag_removed, (category, intensity)) or
    (text, None) if no valid tag is present — the model won't always
    include one, and that's fine, it just means no mood update this turn.
    """
    match = None
    for m in _MOOD_TAG_RE.finditer(text):
        match = m  # last match wins, in case of stray earlier lines

    if not match:
        return text.strip(), None

    category = match.group(1).lower()
    clean = (text[:match.start()] + text[match.end():]).strip()

    if category not in CATEGORIES:
        return clean, None

    return clean, (category, int(match.group(2)))
