from brain.limbic.state import LimbicSystem
from brain.limbic.mood import Mood


def test_starts_with_a_valid_mood():
    limbic = LimbicSystem()
    assert 1 <= limbic.current.intensity <= 3


def test_wake_returns_and_sets_new_mood():
    limbic = LimbicSystem()
    mood = limbic.wake()
    assert limbic.current == mood


def test_same_category_drifts_intensity_up_by_one_step():
    limbic = LimbicSystem()
    limbic.current = Mood("happy", 1)

    limbic.react("happy", 3)

    assert limbic.current == Mood("happy", 2)


def test_same_category_drifts_intensity_down_by_one_step():
    limbic = LimbicSystem()
    limbic.current = Mood("happy", 3)

    limbic.react("happy", 1)

    assert limbic.current == Mood("happy", 2)


def test_different_category_mild_reading_fades_current():
    limbic = LimbicSystem()
    limbic.current = Mood("happy", 2)

    limbic.react("sad", 1)

    assert limbic.current == Mood("happy", 1)


def test_different_category_mild_reading_at_min_intensity_switches():
    limbic = LimbicSystem()
    limbic.current = Mood("happy", 1)

    limbic.react("sad", 1)

    assert limbic.current == Mood("sad", 1)


def test_different_category_intense_reading_takes_over():
    limbic = LimbicSystem()
    limbic.current = Mood("calm", 1)

    limbic.react("scared", 3)

    assert limbic.current == Mood("scared", 3)
