"""
The vocabulary a scenario is written in. A scenario is just a list of
these. Say/EndSession/Restart change the world; the Expect* steps check
it — against internal state (mood, long term memory) wherever possible,
since the model's exact wording changes between runs but whether a fact
got stored/recalled or a mood actually shifted does not.
"""

from dataclasses import dataclass


@dataclass
class Say:
    """Send one message to the brain, as the user."""
    text: str


@dataclass
class EndSession:
    """Force the session to end and the rest process to run, synchronously."""


@dataclass
class Restart:
    """Simulate a reboot: a brand new RobotBrain against the same storage."""


@dataclass
class SetMood:
    """Test-only: seed a known starting mood instead of the random wake
    mood. Mood-shift assertions need this — without it you're checking
    against an unknown random starting point, not the effect you're
    actually trying to test."""
    category: str
    intensity: int = 1


@dataclass
class ExpectReplyContains:
    """Check the most recent reply for a substring. Case-insensitive by default —
    keep this for things that must literally be echoed back (like a name)."""
    substring: str
    case_sensitive: bool = False


@dataclass
class ExpectMood:
    """Check the brain's current mood. Leave a field None to skip that check."""
    category: str = None
    min_intensity: int = None
    exclude_categories: tuple = None


@dataclass
class ExpectLongTermRecall:
    """Query long term memory and check that at least one hit mentions substring."""
    query: str
    substring: str
