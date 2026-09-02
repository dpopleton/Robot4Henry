#!/usr/bin/env python3
"""
Run a scripted conversation against the real brain and watch it play out
turn by turn, with pass/fail on each check — a repeatable way to answer
"is the program actually behaving correctly" instead of manually typing
the same conversation into main.py every time.

Usage:
    python run_scenario.py --list
    python run_scenario.py remembers_name_across_sessions
    python run_scenario.py mood_shifts_when_angered --real-storage
"""

import argparse
import os
import sys

# tests/ has no __init__.py, so it only resolves as a namespace package if
# this script's own directory is on sys.path — not guaranteed depending on
# how python was invoked. Same fix wipe_memory.py already uses for config/.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.scenarios import conversations
from tests.scenarios.isolation import isolated_brain_factory
from tests.scenarios.runner import run_scenario


def main():
    parser = argparse.ArgumentParser(description="Run a Qbot conversation scenario")
    parser.add_argument("name", nargs="?", help="scenario name (see --list)")
    parser.add_argument("--list", action="store_true", help="list available scenarios and exit")
    parser.add_argument(
        "--real-storage", action="store_true",
        help="use storage/robot.db and storage/chroma_db instead of a disposable temp dir"
    )
    args = parser.parse_args()

    if args.list or not args.name:
        print("Available scenarios:")
        for name in conversations.SCENARIOS:
            print(f"  - {name}")
        return 0 if args.list else 1

    if args.name not in conversations.SCENARIOS:
        print(f"Unknown scenario: {args.name!r}\n")
        print("Available scenarios:")
        for name in conversations.SCENARIOS:
            print(f"  - {name}")
        return 1

    if args.real_storage:
        from brain.cognition.robot_brain import RobotBrain
        make_brain = RobotBrain
    else:
        make_brain = isolated_brain_factory()

    steps = conversations.SCENARIOS[args.name]()
    print(f"=== Running scenario: {args.name} ===\n")
    result = run_scenario(make_brain, steps, verbose=True)

    print("=" * 40)
    if result.passed:
        print(f"PASS — all {len(result.checks)} checks passed.")
        return 0

    print(f"FAIL — {len(result.failures())}/{len(result.checks)} checks failed:")
    for desc, detail in result.failures():
        print(f"  - {desc}\n    {detail}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
