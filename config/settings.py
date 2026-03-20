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
DB_PATH = "storage/robot.db"
CHROMA_PATH = "storage/chroma_db"

# Ollama
OLLAMA_HOST = "http://localhost:11434"