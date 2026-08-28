import pytest
from brain.memory.short_term import ShortTermMemory


@pytest.fixture
def mem():
    return ShortTermMemory(max_exchanges=3)


def test_add_messages(mem):
    mem.add("user", "Hello")
    result = mem.add("assistant", "Hi there")
    assert result is None  # no eviction yet
    assert mem.exchange_count() == 1


def test_no_eviction_under_limit(mem):
    for i in range(3):
        mem.add("user", f"Message {i}")
        result = mem.add("assistant", f"Response {i}")
    assert result is None
    assert mem.exchange_count() == 3


def test_eviction_at_limit(mem):
    for i in range(3):
        mem.add("user", f"Message {i}")
        mem.add("assistant", f"Response {i}")

    mem.add("user", "Message 3")
    evicted = mem.add("assistant", "Response 3")

    assert evicted is not None
    assert evicted[0]["content"] == "Message 0"
    assert evicted[1]["content"] == "Response 0"


def test_eviction_slides_window(mem):
    for i in range(4):
        mem.add("user", f"Message {i}")
        mem.add("assistant", f"Response {i}")

    messages = mem.get_messages()
    assert messages[0]["content"] == "Message 1"
    assert mem.exchange_count() == 3


def test_clear_resets(mem):
    mem.add("user", "Hello")
    mem.add("assistant", "Hi")
    mem.clear()
    assert len(mem) == 0
    assert mem.exchange_count() == 0


def test_user_message_never_triggers_eviction(mem):
    for i in range(3):
        mem.add("user", f"Message {i}")
        mem.add("assistant", f"Response {i}")

    # Adding user message alone should not evict
    result = mem.add("user", "One more")
    assert result is None