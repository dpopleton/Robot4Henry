import pytest
from brain.limbic.mood import Mood, CATEGORIES, random_wake_mood


def test_valid_mood_constructs():
    mood = Mood("happy", 2)
    assert mood.category == "happy"
    assert mood.intensity == 2


def test_invalid_category_raises():
    with pytest.raises(ValueError):
        Mood("furious", 2)


def test_invalid_intensity_raises():
    with pytest.raises(ValueError):
        Mood("happy", 5)


def test_describe_calm_mild():
    assert Mood("calm", 1).describe() == "calm"


def test_describe_calm_intense():
    assert Mood("calm", 3).describe() == "deeply relaxed"


def test_describe_other_category():
    assert Mood("angry", 3).describe() == "very angry"
    assert Mood("sad", 1).describe() == "a little sad"


def test_random_wake_mood_is_valid():
    for _ in range(50):
        mood = random_wake_mood()
        assert mood.category in CATEGORIES
        assert 1 <= mood.intensity <= 3
