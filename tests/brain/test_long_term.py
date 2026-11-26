"""LongTermMemory against a real ChromaDB (with a fake embedding)."""
from brain.memory.long_term import LongTermMemory
from tests.brain.fake_embedding import FakeEmbedding


def _memory(tmp_path):
    return LongTermMemory(chroma_path=str(tmp_path / "chroma"), embedding_function=FakeEmbedding())


def _session_docs(memory, session_id):
    got = memory.collection.get(where={"session_id": session_id})
    return sorted(got["documents"]), sorted(got["ids"])


def test_replace_session_stores_with_stable_ids(tmp_path):
    memory = _memory(tmp_path)
    memory.replace_session("s1", ["Henry built a Lego castle.", "Henry has a cat."])

    docs, ids = _session_docs(memory, "s1")
    assert docs == ["Henry built a Lego castle.", "Henry has a cat."]
    assert ids == ["s1-0", "s1-1"]


def test_re_resting_a_session_replaces_rather_than_duplicates(tmp_path):
    memory = _memory(tmp_path)
    memory.replace_session("s1", ["Henry built a Lego castle.", "Henry has a cat."])
    # A re-run after a crash: same session, the model words it differently
    # and lists fewer memories.
    memory.replace_session("s1", ["Henry made a castle out of Lego."])

    docs, _ = _session_docs(memory, "s1")
    assert docs == ["Henry made a castle out of Lego."]
    assert memory.count() == 1


def test_replacing_with_nothing_clears_the_session(tmp_path):
    memory = _memory(tmp_path)
    memory.replace_session("s1", ["Henry built a Lego castle."])
    memory.replace_session("s1", [])
    assert memory.count() == 0


def test_replace_leaves_other_sessions_alone(tmp_path):
    memory = _memory(tmp_path)
    memory.replace_session("s1", ["Henry built a Lego castle."])
    memory.replace_session("s2", ["Henry likes dinosaurs."])
    memory.replace_session("s1", ["Henry built a Lego tower."])

    assert _session_docs(memory, "s2")[0] == ["Henry likes dinosaurs."]
    assert memory.count() == 2


def test_metadata_is_kept_and_session_id_wins(tmp_path):
    memory = _memory(tmp_path)
    memory.replace_session("s1", ["Henry has a cat."],
                           metadata={"created_at": "2026-11-23", "session_id": "wrong"})
    got = memory.collection.get(ids=["s1-0"])
    assert got["metadatas"][0] == {"created_at": "2026-11-23", "session_id": "s1"}


def test_memories_survive_reopening(tmp_path):
    _memory(tmp_path).replace_session("s1", ["Henry has a cat."])
    assert _memory(tmp_path).retrieve("cat") == ["Henry has a cat."]
