from typing import List, Optional
from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str


class Source(BaseModel):
    rank: int
    score: float
    file_name: str
    page: Optional[int] = None
    category: Optional[str] = None
    chunk_id: Optional[int] = None
    preview: str


class QueryResponse(BaseModel):
    answer: str
    retriever: str
    latency: float
    contexts: List[str]
    sources: List[Source]
