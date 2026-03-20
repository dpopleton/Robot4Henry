import tempfile
import pytest
import os
from core.memory.key_facts import KeyFactsStore

TEST_DB = "storage/test_facts.db"


@pytest.fixture
def store():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    s = KeyFactsStore(db_path=db_path)
    yield s
    s.conn.close()
    os.remove(db_path)


def test_set_and_get(store):
    store.set("name", "Henry")
    assert store.get("name") == "Henry"


def test_overwrite(store):
    store.set("name", "Henry")
    store.set("name", "Henry Smith")
    assert store.get("name") == "Henry Smith"


def test_get_missing_returns_none(store):
    assert store.get("nonexistent") is None


def test_get_all(store):
    store.set("name", "Henry")
    store.set("age", "5")
    facts = store.get_all()
    assert facts["name"] == "Henry"
    assert facts["age"] == "5"


def test_format_for_prompt(store):
    store.set("name", "Henry")
    formatted = store.format_for_prompt()
    assert "KEY FACTS" in formatted
    assert "Henry" in formatted


def test_delete(store):
    store.set("name", "Henry")
    store.delete("name")
    assert store.get("name") is None


def test_empty_format_returns_empty_string(store):
    assert store.format_for_prompt() == ""