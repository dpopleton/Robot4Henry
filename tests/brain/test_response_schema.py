from brain.cognition.response_schema import parse_chat_response


def test_parses_valid_response():
    raw = '{"reply": "That sounds like fun!", "mood": {"category": "happy", "intensity": 2}}'

    reply, mood = parse_chat_response(raw)

    assert reply == "That sounds like fun!"
    assert mood == ("happy", 2)


def test_category_is_case_insensitive():
    raw = '{"reply": "Hi!", "mood": {"category": "Curious", "intensity": 3}}'

    reply, mood = parse_chat_response(raw)

    assert mood == ("curious", 3)


def test_missing_mood_field_keeps_reply_no_signal():
    raw = '{"reply": "That sounds like fun!"}'

    reply, mood = parse_chat_response(raw)

    assert reply == "That sounds like fun!"
    assert mood is None


def test_unknown_category_keeps_reply_no_signal():
    raw = '{"reply": "Hello there.", "mood": {"category": "furious", "intensity": 2}}'

    reply, mood = parse_chat_response(raw)

    assert reply == "Hello there."
    assert mood is None


def test_out_of_range_intensity_keeps_reply_no_signal():
    raw = '{"reply": "Hi!", "mood": {"category": "happy", "intensity": 5}}'

    reply, mood = parse_chat_response(raw)

    assert reply == "Hi!"
    assert mood is None


def test_non_integer_intensity_keeps_reply_no_signal():
    raw = '{"reply": "Hi!", "mood": {"category": "happy", "intensity": true}}'

    reply, mood = parse_chat_response(raw)

    assert reply == "Hi!"
    assert mood is None


def test_malformed_json_falls_back_to_raw_text_as_reply():
    raw = "Oops, not JSON at all."

    reply, mood = parse_chat_response(raw)

    assert reply == "Oops, not JSON at all."
    assert mood is None


def test_empty_reply_falls_back_to_raw_text():
    raw = '{"reply": "", "mood": {"category": "happy", "intensity": 1}}'

    reply, mood = parse_chat_response(raw)

    assert reply == raw
    assert mood is None
