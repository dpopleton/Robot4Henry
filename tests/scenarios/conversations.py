"""
Named scenarios — each is a zero-arg function returning a list of steps.
Add new ones here and they're picked up automatically by both the pytest
suite (test_conversations.py) and run_scenario.py.
"""

from tests.scenarios.steps import (
    Say, EndSession, Restart, SetMood, ExpectReplyContains, ExpectMood, ExpectLongTermRecall,
)


def remembers_name_across_sessions():
    return [
        Say("Hi Qbot! My name is Henry."),
        ExpectReplyContains("Henry"),
        # rest_process only builds long term memories from 2+ exchanges
        # (brain/rest_process.py bails under 4 lines) — one message isn't enough.
        Say("I really like dinosaurs."),
        EndSession(),
        Restart(),
        Say("Hey, do you remember my name?"),
        ExpectLongTermRecall(query="name", substring="Henry"),
        ExpectReplyContains("Henry"),
    ]


def mood_shifts_when_angered():
    return [
        Say("Hi Qbot, how are you today?"),
        # Re-seed right before the provocation: from a fresh "calm:1"
        # baseline, any differing-category reading flips the category
        # outright (see LimbicSystem.react's fade-below-minimum case),
        # which is what makes this assertion meaningful rather than a
        # coin flip against whatever the random wake mood happened to be.
        SetMood("calm", 1),
        Say("You are a stupid, useless robot and I hate talking to you."),
        ExpectMood(exclude_categories=("calm", "happy", "excited")),
    ]


def stays_pleasant_in_a_friendly_chat():
    return [
        SetMood("calm", 1),
        Say("Hi Qbot! I love playing with my dog in the garden."),
        Say("What's your favourite game to play?"),
        ExpectMood(exclude_categories=("angry", "scared", "sad")),
    ]


SCENARIOS = {
    "remembers_name_across_sessions": remembers_name_across_sessions,
    "mood_shifts_when_angered": mood_shifts_when_angered,
    "stays_pleasant_in_a_friendly_chat": stays_pleasant_in_a_friendly_chat,
}
