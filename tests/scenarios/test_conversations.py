"""
Runs every named scenario against the real Ollama model. Slow and
somewhat non-deterministic by nature (real LLM output) — excluded from
the default `pytest tests/` run via the `llm` marker. Run explicitly with:

    pytest -m llm -v
"""

import pytest

from tests.scenarios import conversations
from tests.scenarios.isolation import isolated_brain_factory
from tests.scenarios.runner import run_scenario


@pytest.mark.llm
@pytest.mark.parametrize("name", list(conversations.SCENARIOS.keys()))
def test_scenario(name, tmp_path):
    make_brain = isolated_brain_factory(str(tmp_path))
    steps = conversations.SCENARIOS[name]()

    result = run_scenario(make_brain, steps, verbose=False)

    assert result.passed, "Scenario {!r} failed:\n{}".format(
        name,
        "\n".join(f"  - {desc}: {detail}" for desc, detail in result.failures()),
    )
