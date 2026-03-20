import pytest
from unittest.mock import MagicMock
from core.memory.medium_term import MediumTermMemory


@pytest.fixture
def llm():
    mock = MagicMock()
    mock.complete.return_value = "Summary of conversation so far."
    return mock


@pytest.fixture
def mem(llm):
    return MediumTermMemory(llm_client=llm)


def test_empty_on_init(mem):
    assert mem.get() == ""
    assert not mem.has_content()
    assert mem.format_for_prompt() == ""


def test_update_creates_summary(mem, llm):
    evicted = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"}
    ]
    mem.update(evicted)
    assert mem.has_content()
    assert llm.complete.called


def test_update_empty_does_nothing(mem, llm):
    mem.update([])
    assert not mem.has_content()
    assert not llm.complete.called


def test_incremental_update(mem, llm):
    llm.complete.side_effect = [
        "First summary.",
        "Updated summary."
    ]

    mem.update([
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"}
    ])
    mem.update([
        {"role": "user", "content": "How are you?"},
        {"role": "assistant", "content": "I am well"}
    ])

    # Second call should include existing summary
    second_call_prompt = llm.complete.call_args_list[1][0][0]
    assert "First summary." in second_call_prompt
    assert mem.get() == "Updated summary."


def test_format_for_prompt(mem, llm):
    mem.update([
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"}
    ])
    formatted = mem.format_for_prompt()
    assert "EARLIER IN THIS CONVERSATION" in formatted


def test_clear_wipes_summary(mem, llm):
    mem.update([
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"}
    ])
    mem.clear()
    assert not mem.has_content()
    assert mem.get() == ""