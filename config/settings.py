import os
import warnings
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Hardware ports.  Keep these as stable USB identities: ttyACM numbers change
# whenever a Pico is unplugged or a hub enumerates in a different order.
def _serial_by_id_setting(name: str):
    port = os.environ.get(name)
    if port is not None and not port.startswith("/dev/serial/by-id/"):
        warnings.warn(
            f"{name} should be a /dev/serial/by-id/... path; falling back to mock (got {port!r})",
            stacklevel=2,
        )
        return None
    return port


EYES_PORT = _serial_by_id_setting("QBOT_EYES_PORT")
CROWN_PORT = _serial_by_id_setting("QBOT_CROWN_PORT")
MOUTH_PORT = _serial_by_id_setting("QBOT_MOUTH_PORT")
LIGHTS_PORT = _serial_by_id_setting("QBOT_LIGHTS_PORT")


# Model configuration
PRIMARY_MODEL = "llama3.2:1b"
                #This one took forever thingking. "qwen3.5:0.8b"
# REASONING_MODEL = llama3.2:1b
# REASONING_MODEL = "phi3:mini" #too big
# REASONING_MODEL = "phi3:mini" #too big

# Memory configuration
SHORT_TERM_MAX_EXCHANGES = 10
LONG_TERM_RETRIEVE_COUNT = 3

# Session configuration
SESSION_TIMEOUT_SECONDS = 300  # 5 minutes

# Storage paths
DB_PATH = os.environ.get("QBOT_DB_PATH", str(BASE_DIR / "storage" / "robot.db"))
CHROMA_PATH = os.environ.get("QBOT_CHROMA_PATH", str(BASE_DIR / "storage" / "chroma_db"))
# Qbot's voice: the Piper model Henry chose (R-307).
VOICE_MODEL = os.environ.get(
    "QBOT_VOICE_MODEL", str(BASE_DIR / "storage" / "voices" / "en_GB-northern_english_male-medium.onnx")
)

# Ollama
OLLAMA_HOST = "http://localhost:11434"
