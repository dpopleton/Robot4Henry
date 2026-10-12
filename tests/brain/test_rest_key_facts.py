"""Key fact extraction in the rest process, with the LLM replaced by canned
replies taken from real llama3.2:1b output."""
import os
import tempfile
from unittest.mock import MagicMock

import pytest

from brain.memory.key_facts import KeyFactsStore
from brain.rest_process import RestProcess

CONVERSATION = (
    "USER: Hi Qbot! My name is Henry.\n"
    "ASSISTANT: Hi Henry! Do you like pizza?\n"
    "USER: I really like dinosaurs."
)


@pytest.fixture
def store():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    s = KeyFactsStore(db_path=db_path)
    yield s
    s.conn.close()
    os.remove(db_path)


def extract(store, llm_reply):
    llm = MagicMock()
    llm.complete.return_value = llm_reply
    rest = RestProcess(llm, raw_logger=MagicMock(), long_term=MagicMock(), key_facts=store)
    rest._extract_key_facts(CONVERSATION)
    return llm


def test_none_line_does_not_discard_real_facts(store):
    extract(store, "name: Henry\nfavourite animal: dinosaur\npets: NONE\nage: NONE")
    assert store.get_all() == {"name": "Henry", "favourite animal": "dinosaur"}


def test_invented_facts_are_rejected(store):
    extract(store, "name: Henry\nfavourite food: sushi\nage: 30\nfavourite colour: blue\nage: ")
    assert store.get_all() == {"name": "Henry"}


def test_facts_only_the_assistant_said_are_rejected(store):
    extract(store, "favourite food: pizza")
    assert store.get_all() == {}


def test_bare_none_stores_nothing(store):
    extract(store, "NONE")
    assert store.get_all() == {}


def test_extraction_runs_at_temperature_zero(store):
    llm = extract(store, "NONE")
    assert llm.complete.call_args.kwargs["options"] == {"temperature": 0}


@pytest.mark.parametrize("value, grounded", [
    ("Henry", True),
    ("dinosaur", True),       # user said "dinosaurs"
    ("dinosaurs", True),
    ("pizza", False),         # only the assistant said it
    ("30", False),
    ("", False),
])
def test_is_grounded(value, grounded):
    user_lines = RestProcess._user_only(None, CONVERSATION)
    assert RestProcess._is_grounded(value, user_lines) is grounded
