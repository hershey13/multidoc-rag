import time
from collections import defaultdict
from typing import List

from langchain_core.documents import Document

from src.config import (
    HYBRID_RETRIEVER,
    RRF_SCORE,
    INITIAL_RETRIEVAL_K,
    RERANK_TOP_K,
    RERANKER_MODEL,
)

from src.retrievers.schemas import (
    RetrievalResult,
    RetrievalResponse,
)

from src.retrievers.dense import DenseRetriever
from src.retrievers.sparse import SparseRetriever
from src.models.reranker import CrossEncoderReranker


class HybridRRFRetriever:

    def __init__(
        self,
        chunks: List[Document],
        k: int = RERANK_TOP_K,
        rrf_k: int = 60,
        persist_directory: str | None = None,
    ):

        self.k = k
        self.rrf_k = rrf_k

        # Retrieve many candidates
        self.dense = DenseRetriever(
            k=INITIAL_RETRIEVAL_K,
            persist_directory=persist_directory,
        )

        self.sparse = SparseRetriever(chunks)

        # Load CrossEncoder ONLY ONCE
        self.reranker = CrossEncoderReranker(RERANKER_MODEL)

    def dense_search(self, query):
        return self.dense.search_with_scores(query)

    def sparse_search(self, query):
        return self.sparse.search_with_scores(
            query,
            k=INITIAL_RETRIEVAL_K,
        )

    def search_with_scores(
        self,
        query: str,
        alpha: float = 0.5,
    ) -> RetrievalResponse:

        start = time.perf_counter()

        dense_response = self.dense_search(query)

        sparse_response = self.sparse_search(query)

        response = self.fuse_results_rrf(
            query=query,
            dense_response=dense_response,
            sparse_response=sparse_response,
        )

        response.latency = time.perf_counter() - start

        return response

    def get_chunk_key(self, result):
        return (
            f"{result.document.metadata['doc_id']}"
            f"_chunk_{result.document.metadata['chunk_id']}"
        )

    def fuse_results_rrf(
        self,
        query: str,
        dense_response,
        sparse_response,
    ) -> RetrievalResponse:

        rrf_scores = defaultdict(float)
        lookup = {}

        # Dense
        for result in dense_response.results:

            key = self.get_chunk_key(result)

            rrf_scores[key] += 1 / (self.rrf_k + result.rank)

            lookup[key] = result

        # Sparse
        for result in sparse_response.results:

            key = self.get_chunk_key(result)

            rrf_scores[key] += 1 / (self.rrf_k + result.rank)

            if key not in lookup:
                lookup[key] = result

        ranked = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        # Keep many candidates for reranking
        ranked = ranked[:INITIAL_RETRIEVAL_K]

        retrieval_results = []

        for rank, (key, score) in enumerate(
            ranked,
            start=1,
        ):

            result = lookup[key]

            retrieval_results.append(
                RetrievalResult(
                    rank=rank,
                    retrieval_score=float(score),
                    score_type=RRF_SCORE,
                    retriever=HYBRID_RETRIEVER,
                    document=result.document,
                )
            )

        # CrossEncoder reranking
        reranked = self.reranker.rerank(
            query=query,
            retrieval_results=retrieval_results,
            top_k=self.k,
        )

        for rank, result in enumerate(
            reranked,
            start=1,
        ):
            result.rank = rank

        return RetrievalResponse(
            query=query,
            retriever=HYBRID_RETRIEVER,
            latency=0.0,
            results=reranked,
        )

    def summary(self):

        print("\n")
        print(" HYBRID RRF RETRIEVER ".center(70, "="))
        print(f"Initial Retrieval : {INITIAL_RETRIEVAL_K}")
        print(f"Final Top K       : {self.k}")
        print(f"RRF K             : {self.rrf_k}")
        print(f"Reranker          : {RERANKER_MODEL}")
        print("=" * 70)
