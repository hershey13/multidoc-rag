from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

TOP_K = 5

SEARCH_TYPE = "similarity"

DEFAULT_COLLECTION = "multidoc_rag"

VECTOR_DB_PATH = BASE_DIR / "chroma_db"

DATA_DIR = BASE_DIR / "data" / "corpus"

# Retriever Names
DENSE_RETRIEVER = "Dense"
SPARSE_RETRIEVER = "Sparse"
HYBRID_RETRIEVER = "Hybrid"

# Score Types
COSINE_DISTANCE = "cosine_distance"
BM25_SCORE = "bm25_score"
RRF_SCORE = "rrf_score"
HYBRID_SCORE = "hybrid_score"

# Hybrid Retrieval
HYBRID_ALPHA = 0.5
HYBRID_BETA = 0.5

# Cross Encoder
INITIAL_RETRIEVAL_K = 40
RERANK_TOP_K = 5
RERANKER_MODEL = "BAAI/bge-reranker-base"
