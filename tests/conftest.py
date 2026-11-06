"""Keep every test away from the real storage/.

Set before any test module imports config.settings, so even code that
falls back to the default DB_PATH / CHROMA_PATH (bound at import time as
default arguments) writes to a throwaway directory, never storage/robot.db.
"""
import os
import tempfile
from pathlib import Path

_test_storage = Path(tempfile.mkdtemp(prefix="qbot_tests_"))
os.environ["QBOT_DB_PATH"] = str(_test_storage / "robot.db")
os.environ["QBOT_CHROMA_PATH"] = str(_test_storage / "chroma_db")
