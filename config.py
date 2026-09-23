from pathlib import Path


from pathlib import Path

BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "dataset"

PDF_PATH = DATA_DIR / "tech_jds_149.pdf"



CHUNK_SIZE = 800
CHUNK_OVERLAP = 150




EMBEDDING_MODEL = "jina-embeddings-v5-text-small"

LLM_MODEL= "gemini-3.1-flash-lite"


COLLECTION_NAME = "job_profile"