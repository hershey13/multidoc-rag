from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data" / "corpus"

VECTOR_DB_PATH = BASE_DIR / "chroma_db"

TOP_K = 5
RETRIEVER = "hybrid_rrf"

LLM_PROVIDER = "groq"
TEMPERATURE = 0

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"

OLLAMA_MODEL = "llama3.1:8b"
