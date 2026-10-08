"""The generated docs indexes (roadmap, decisions, journal) must match
their source files, and the front matter must be valid — so an agent or
human editing an item can't leave the overview stale or a broken link."""

import importlib.util
import os

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
_spec = importlib.util.spec_from_file_location("build_index", os.path.join(ROOT, "docs", "build_index.py"))
build_index = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_index)


def _sources():
    return (
        build_index._load(build_index.ITEMS_DIR, "R-"),
        build_index._load(build_index.DECISIONS_DIR, "D-"),
        build_index.load_phases(),
    )


def test_front_matter_is_valid():
    assert build_index.validate(*_sources()) == []


def test_generated_indexes_are_up_to_date():
    assert build_index.stale_files() == [], "run: python docs/build_index.py"


def test_validation_catches_broken_references():
    items, decisions, phases = _sources()
    broken = dict(items[0], depends_on=["R-999"], decisions=["D-999"], status="wip")
    errors = build_index.validate([broken] + items[1:], decisions, phases)
    assert any("R-999" in e for e in errors)
    assert any("D-999" in e for e in errors)
    assert any("unknown status" in e for e in errors)
