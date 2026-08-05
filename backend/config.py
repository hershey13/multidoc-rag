from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# Project Paths
# =====================================================

# backend/
BASE_DIR = Path(__file__).resolve().parent

# internship project/
PROJECT_ROOT = BASE_DIR.parent

# =====================================================
# Data
# =====================================================

DATA_DIR = PROJECT_ROOT / "multidoc-rag" / "data" / "corpus"

# =====================================================
# ChromaDB
# =====================================================

VECTOR_DB_PATH = (
    PROJECT_ROOT
    / "multidoc-rag"
    / "notebook"
    / "experiments"
    / "2_hybrid_rrf_crossencoder_recursive700"
    / "chroma_db"
)

# =====================================================
# Retrieval
# =====================================================

TOP_K = 5

RETRIEVER = "hybrid_rrf"

# =====================================================
# LLM
# =====================================================

LLM_PROVIDER = "groq"
# Options:
# "groq"
# "ollama"

TEMPERATURE = 0

# =====================================================
# Groq
# =====================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.1-8b-instant"

# =====================================================
# Ollama
# =====================================================

OLLAMA_MODEL = "llama3.1:8b"

# =====================================================
# Debug
# =====================================================

print("=" * 70)
print("Configuration")
print("=" * 70)

print(f"Project Root : {PROJECT_ROOT}")
print(f"Data Path    : {DATA_DIR}")
print(f"Data Exists  : {DATA_DIR.exists()}")

print(f"Vector DB    : {VECTOR_DB_PATH}")
print(f"DB Exists    : {VECTOR_DB_PATH.exists()}")

print("=" * 70)
