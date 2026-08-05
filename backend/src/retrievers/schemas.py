from dataclasses import dataclass
from typing import List
from langchain_core.documents import Document


@dataclass
class RetrievalResult:
    rank: int
    retrieval_score: float
    score_type: str
    retriever: str
    document: Document


@dataclass
class RetrievalResponse:
    query: str
    retriever: str
    latency: float
    results: List[RetrievalResult]
