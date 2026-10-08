"""anatomy/<part>/ must stay machine-readable — the brain will eventually
look parts up from it (R-905)."""

import glob
import os

import pytest
import yaml

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
PARTS = sorted(glob.glob(os.path.join(ROOT, "anatomy", "*", "part.yaml")))
ITEM_IDS = {os.path.basename(p).split("-")[0] + "-" + os.path.basename(p).split("-")[1]
            for p in glob.glob(os.path.join(ROOT, "docs", "roadmap", "items", "R-*.md"))}
STATUSES = {"idea", "designing", "building", "built"}


@pytest.mark.parametrize("path", PARTS, ids=lambda p: os.path.basename(os.path.dirname(p)))
def test_part_yaml(path):
    part = yaml.safe_load(open(path))
    folder = os.path.basename(os.path.dirname(path))
    assert part["name"] == folder
    assert part["aliases"] and folder in part["aliases"]
    assert part["status"] in STATUSES
    assert part["summary_for_henry"].strip()
    assert isinstance(part["henry_text_approved"], bool)
    for ref in part.get("roadmap") or []:
        assert ref in ITEM_IDS, f"{folder}: roadmap item {ref} doesn't exist"


@pytest.mark.parametrize("path", PARTS, ids=lambda p: os.path.basename(os.path.dirname(p)))
def test_manifest_images_exist(path):
    folder = os.path.dirname(path)
    manifest = yaml.safe_load(open(os.path.join(folder, "manifest.yaml"))) or {}
    for entry in manifest.get("images") or []:
        assert os.path.exists(os.path.join(folder, entry["file"])), entry["file"]
        if entry.get("model"):
            assert os.path.exists(os.path.join(folder, entry["model"])), entry["model"]


def test_aliases_are_unique_across_parts():
    seen = {}
    for path in PARTS:
        part = yaml.safe_load(open(path))
        for alias in part["aliases"]:
            assert alias not in seen, f"alias {alias!r} used by both {seen[alias]} and {part['name']}"
            seen[alias] = part["name"]
