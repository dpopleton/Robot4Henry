import random
from dataclasses import dataclass

CATEGORIES = ("calm", "happy", "curious", "excited", "sleepy", "sad", "scared", "angry")
MIN_INTENSITY = 1
MAX_INTENSITY = 3

# Waking mood is random but weighted — mostly calm/happy/curious, rarely
# starting out furious. Mirrors how you don't usually wake up at full
# emotional intensity.
_WAKE_CATEGORY_WEIGHTS = {
    "calm": 30, "happy": 25, "curious": 15, "excited": 10,
    "sleepy": 10, "sad": 5, "scared": 3, "angry": 2,
}
_WAKE_INTENSITY_WEIGHTS = {1: 60, 2: 30, 3: 10}

_QUALIFIERS = {1: "a little", 2: "quite", 3: "very"}


@dataclass(frozen=True)
class Mood:
    category: str = "calm"
    intensity: int = 1

    def __post_init__(self):
        if self.category not in CATEGORIES:
            raise ValueError(f"Unknown mood category: {self.category!r}")
        if not (MIN_INTENSITY <= self.intensity <= MAX_INTENSITY):
            raise ValueError(f"Intensity must be {MIN_INTENSITY}-{MAX_INTENSITY}, got {self.intensity}")

    def describe(self) -> str:
        """Natural-language description for the personality prompt."""
        if self.category == "calm":
            return "calm" if self.intensity == 1 else "deeply relaxed"
        return f"{_QUALIFIERS[self.intensity]} {self.category}"


def random_wake_mood() -> Mood:
    category = random.choices(
        list(_WAKE_CATEGORY_WEIGHTS.keys()),
        weights=list(_WAKE_CATEGORY_WEIGHTS.values()),
    )[0]
    intensity = random.choices(
        list(_WAKE_INTENSITY_WEIGHTS.keys()),
        weights=list(_WAKE_INTENSITY_WEIGHTS.values()),
    )[0]
    return Mood(category, intensity)
