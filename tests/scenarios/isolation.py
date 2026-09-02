import tempfile
from pathlib import Path

from brain.cognition.robot_brain import RobotBrain


def isolated_brain_factory(base_dir: str = None):
    """Returns a zero-arg factory building a RobotBrain against a fresh
    directory, so scenario runs never touch real storage/robot.db."""
    tmp_dir = Path(base_dir) if base_dir else Path(tempfile.mkdtemp(prefix="qbot_scenario_"))
    db_path = str(tmp_dir / "robot.db")
    chroma_path = str(tmp_dir / "chroma_db")

    def make_brain():
        return RobotBrain(db_path=db_path, chroma_path=chroma_path)

    return make_brain
