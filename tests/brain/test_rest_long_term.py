from unittest.mock import MagicMock
from brain.rest_process import RestProcess

CONVERSATION_4_LINES = (
    "USER: Hi Qbot!\n"
    "ASSISTANT: Hello Henry!\n"
    "USER: I made a Lego castle today.\n"
    "ASSISTANT: Wow, what kind of castle?"
)


def _build_rest(llm_reply: str):
    llm = MagicMock()
    llm.complete.return_value = llm_reply
    long_term = MagicMock()
    rest = RestProcess(llm=llm, raw_logger=MagicMock(), long_term=long_term, key_facts=MagicMock())
    return rest, llm, long_term


def test_bare_none_stores_no_long_term_memories():
    rest, _, long_term = _build_rest("NONE")
    rest._build_long_term_memories(CONVERSATION_4_LINES, "session-123")
    assert long_term.store.call_count == 0


def test_sentence_with_word_none_is_preserved():
    # Previous bug: any substring "NONE" aborted the entire rest process.
    sentence = "Henry mentioned that none of his toy cars were broken."
    rest, _, long_term = _build_rest(sentence)
    rest._build_long_term_memories(CONVERSATION_4_LINES, "session-123")

    assert long_term.store.call_count == 1
    args, kwargs = long_term.store.call_args
    assert args[0] == sentence
    assert kwargs["metadata"]["session_id"] == "session-123"


def test_none_line_does_not_discard_subsequent_memories():
    reply = "1. NONE\n2. Henry built a tall Lego castle with towers."
    rest, _, long_term = _build_rest(reply)
    rest._build_long_term_memories(CONVERSATION_4_LINES, "session-123")

    assert long_term.store.call_count == 1
    args, _ = long_term.store.call_args
    assert args[0] == "Henry built a tall Lego castle with towers."


def test_preamble_lines_and_headers_are_skipped():
    reply = (
        "Here are the memorable facts from the conversation:\n"
        "1. Henry built a Lego castle.\n"
        "Facts from conversation:\n"
        "2. The assistant asked what kind of castle it was."
    )
    rest, _, long_term = _build_rest(reply)
    rest._build_long_term_memories(CONVERSATION_4_LINES, "session-123")

    stored = [call[0][0] for call in long_term.store.call_args_list]
    assert stored == [
        "Henry built a Lego castle.",
        "The assistant asked what kind of castle it was.",
    ]


def test_short_conversation_under_4_lines_is_skipped():
    short_convo = "USER: Hi\nASSISTANT: Hello\nUSER: Bye"
    rest, llm, long_term = _build_rest("Henry said hi and bye.")
    rest._build_long_term_memories(short_convo, "session-123")

    assert llm.complete.call_count == 0
    assert long_term.store.call_count == 0
