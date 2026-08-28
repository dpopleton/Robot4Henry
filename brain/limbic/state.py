from brain.limbic.mood import Mood, MIN_INTENSITY, MAX_INTENSITY, random_wake_mood


def _step_towards(current: int, target: int) -> int:
    """Move intensity one step towards target — moods drift, they don't snap."""
    if target > current:
        return min(MAX_INTENSITY, current + 1)
    if target < current:
        return max(MIN_INTENSITY, current - 1)
    return current


class LimbicSystem:
    """Tracks the robot's current mood and how it changes turn to turn."""

    def __init__(self):
        self.current = random_wake_mood()

    def wake(self) -> Mood:
        """Called at the start of a new session — a fresh, random mood."""
        self.current = random_wake_mood()
        return self.current

    def react(self, category: str, intensity: int) -> Mood:
        """
        Nudge the current mood based on what this turn's exchange felt
        like. Same feeling reinforced -> intensity drifts towards it.
        A different, mild feeling -> current mood just fades a notch.
        A different, intense feeling -> it takes over outright.
        """
        if category == self.current.category:
            self.current = Mood(category, _step_towards(self.current.intensity, intensity))
        elif intensity >= MAX_INTENSITY:
            self.current = Mood(category, intensity)
        else:
            faded = self.current.intensity - 1
            if faded < MIN_INTENSITY:
                self.current = Mood(category, MIN_INTENSITY)
            else:
                self.current = Mood(self.current.category, faded)
        return self.current
