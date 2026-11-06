import random

from virtual_robot.fake_speech import RATE, sentence_levels


def test_length_and_range():
    levels = sentence_levels(3.0, rand=random.Random(1).random)
    assert len(levels) == 3 * RATE
    assert all(0.0 <= level <= 1.0 for level in levels)


def test_sounds_like_words_with_gaps():
    levels = sentence_levels(4.0, rand=random.Random(2).random)
    assert max(levels) > 0.4
    assert levels.count(0.0) >= 3                       # gaps between words
    assert sum(level > 0.05 for level in levels) > len(levels) / 2   # mostly talking


def test_different_every_time():
    assert sentence_levels(rand=random.Random(1).random) != sentence_levels(rand=random.Random(2).random)
