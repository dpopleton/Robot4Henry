from brain.limbic.parsing import extract_mood_tag


def test_extracts_valid_tag():
    text = "That sounds like fun!\nMOOD: happy:2"

    clean, signal = extract_mood_tag(text)

    assert clean == "That sounds like fun!"
    assert signal == ("happy", 2)


def test_no_tag_returns_none_signal():
    text = "That sounds like fun!"

    clean, signal = extract_mood_tag(text)

    assert clean == "That sounds like fun!"
    assert signal is None


def test_unknown_category_returns_none_signal_but_strips_tag():
    text = "Hello there.\nMOOD: furious:2"

    clean, signal = extract_mood_tag(text)

    assert clean == "Hello there."
    assert signal is None


def test_case_insensitive_and_whitespace_tolerant():
    text = "Hi!\n  mood:   Curious : 3  "

    clean, signal = extract_mood_tag(text)

    assert clean == "Hi!"
    assert signal == ("curious", 3)


def test_out_of_range_intensity_is_not_matched():
    text = "Hi!\nMOOD: happy:5"

    clean, signal = extract_mood_tag(text)

    assert signal is None
    assert "MOOD: happy:5" in clean
