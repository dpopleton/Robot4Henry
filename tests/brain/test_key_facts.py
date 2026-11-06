import tempfile
import pytest
import os
from brain.memory.key_facts import KeyFactsStore

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


def test_close_and_context_manager(tmp_path):
    db_path = str(tmp_path / "cm_facts.db")
    with KeyFactsStore(db_path=db_path) as s:
        s.set("fav_color", "blue")
        assert s.get("fav_color") == "blue"
    # close was called, calling again is idempotent
    s.close()


def test_concurrent_writes(tmp_path):
    import threading
    db_path = str(tmp_path / "concurrent_facts.db")
    store = KeyFactsStore(db_path=db_path)
    errors = []

    def worker(worker_id):
        try:
            for i in range(20):
                store.set(f"key_{worker_id}_{i}", f"val_{worker_id}_{i}")
                assert store.get(f"key_{worker_id}_{i}") == f"val_{worker_id}_{i}"
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    store.close()
    assert not errors, f"Concurrent key facts access raised: {errors}"
