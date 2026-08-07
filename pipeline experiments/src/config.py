"""
Global configuration for the RAG pipeline.
"""

TOP_K = 5

SEARCH_TYPE = "similarity"

DEFAULT_COLLECTION = "multidoc_rag"

VECTOR_DB_PATH = "./chroma_db"

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
HYBRID_ALPHA = 0.5  # Dense weight
HYBRID_BETA = 0.5  # Sparse weight

# Cross Encoder
INITIAL_RETRIEVAL_K = 40
RERANK_TOP_K = 5
RERANKER_MODEL = "BAAI/bge-reranker-base"
