from pathlib import Path

DATA_PATH = Path("data/beca_mec")
CHROMA_PATH = Path("chroma")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "gemini-3.6-flash"

DEFAULT_K = 3