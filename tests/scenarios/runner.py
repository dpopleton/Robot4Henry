"""
Plays a scenario (a list of steps) against a real RobotBrain and
collects pass/fail on every Expect* step, plus a transcript. Used both
by the pytest wrapper (tests/scenarios/test_conversations.py) and by
run_scenario.py for interactive manual runs.
"""

from brain.limbic.mood import Mood
from tests.scenarios.steps import (
    Say, EndSession, Restart, SetMood, ExpectReplyContains, ExpectMood, ExpectLongTermRecall,
)


class ScenarioResult:
    def __init__(self):
        self.checks = []       # (description, passed, detail)
        self.transcript = []   # (speaker, text)

    @property
    def passed(self) -> bool:
        return all(ok for _, ok, _ in self.checks)

    def failures(self):
        return [(desc, detail) for desc, ok, detail in self.checks if not ok]


def run_scenario(make_brain, steps, verbose: bool = False) -> ScenarioResult:
    """make_brain: zero-arg callable returning a fresh RobotBrain against
    whatever storage the caller wants (isolated temp dir, or real storage)."""
    result = ScenarioResult()
    brain = make_brain()
    last_reply = None

    for step in steps:
        if isinstance(step, Say):
            last_reply = brain.chat(step.text)
            result.transcript.append(("user", step.text))
            result.transcript.append(("qbot", last_reply))
            if verbose:
                print(f"You: {step.text}\nQbot: {last_reply}\n")

        elif isinstance(step, EndSession):
            brain.force_rest(blocking=True)
            if verbose:
                print("[session ended — rest process complete]\n")

        elif isinstance(step, Restart):
            brain = make_brain()
            if verbose:
                print("[brain restarted — fresh process, same storage]\n")

        elif isinstance(step, SetMood):
            brain.limbic.current = Mood(step.category, step.intensity)
            if verbose:
                print(f"[mood seeded to {brain.limbic.current}]\n")

        elif isinstance(step, ExpectReplyContains):
            haystack = last_reply if step.case_sensitive else last_reply.lower()
            needle = step.substring if step.case_sensitive else step.substring.lower()
            ok = needle in haystack
            _record(result, f"reply contains {step.substring!r}", ok, last_reply, verbose)

        elif isinstance(step, ExpectMood):
            mood = brain.limbic.current
            ok = True
            if step.category is not None:
                ok = ok and mood.category == step.category
            if step.min_intensity is not None:
                ok = ok and mood.intensity >= step.min_intensity
            if step.exclude_categories is not None:
                ok = ok and mood.category not in step.exclude_categories
            desc = (
                f"mood matches category={step.category!r} "
                f"min_intensity={step.min_intensity!r} exclude={step.exclude_categories!r}"
            )
            _record(result, desc, ok, f"actual mood={mood}", verbose)

        elif isinstance(step, ExpectLongTermRecall):
            memories = brain.long_term.retrieve(step.query)
            found = any(step.substring.lower() in m.lower() for m in memories)
            desc = f"long term recall for {step.query!r} mentions {step.substring!r}"
            _record(result, desc, found, f"retrieved={memories}", verbose)

        else:
            raise TypeError(f"Unknown scenario step: {step!r}")

    return result


def _record(result: ScenarioResult, desc: str, ok: bool, detail, verbose: bool):
    result.checks.append((desc, ok, detail))
    if verbose:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {desc}\n         {detail}\n")
