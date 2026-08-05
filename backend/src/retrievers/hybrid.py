import time
from collections import defaultdict
from typing import List

from langchain_core.documents import Document

from src.config import (
    HYBRID_RETRIEVER,
    HYBRID_SCORE,
)
from src.retrievers.schemas import (
    RetrievalResult,
    RetrievalResponse,
)
from src.retrievers.dense import DenseRetriever
from src.retrievers.sparse import SparseRetriever
from src.models.reranker import CrossEncoderReranker


class HybridRetriever:
    """
    Hybrid retriever combining Dense (ChromaDB) and Sparse (BM25)
    using weighted score fusion.
    """

    def __init__(
        self,
        chunks,
        k=5,
        persist_directory=None,
    ):

        self.k = k

        self.dense = DenseRetriever(
            k=k,
            persist_directory=persist_directory,
        )

        self.sparse = SparseRetriever(chunks)

    def dense_search(
        self,
        query: str,
    ):
        return self.dense.search_with_scores(query)

    def sparse_search(
        self,
        query: str,
    ):
        return self.sparse.search_with_scores(query)

    def normalize_scores(
        self,
        scores,
        reverse=False,
    ):
        """
        Normalize scores to [0,1].

        reverse=True means lower values are better
        (used for cosine distance).
        """

        if not scores:
            return []

        minimum = min(scores)
        maximum = max(scores)

        if maximum == minimum:
            return [1.0] * len(scores)

        normalized = [(score - minimum) / (maximum - minimum) for score in scores]

        if reverse:
            normalized = [1 - score for score in normalized]

        return normalized

    def get_chunk_key(self, result):
        return (
            f"{result.document.metadata['doc_id']}"
            f"_chunk_{result.document.metadata['chunk_id']}"
        )

    def fuse_results(
        self,
        query: str,
        dense_response,
        sparse_response,
        alpha: float = 0.5,
    ) -> RetrievalResponse:

        dense_scores = [r.retrieval_score for r in dense_response.results]

        sparse_scores = [r.retrieval_score for r in sparse_response.results]

        dense_norm = self.normalize_scores(
            dense_scores,
            reverse=True,
        )

        sparse_norm = self.normalize_scores(
            sparse_scores,
        )

        fused_scores = defaultdict(float)

        dense_lookup = {}
        sparse_lookup = {}

        for result, score in zip(
            dense_response.results,
            dense_norm,
        ):

            key = self.get_chunk_key(result)

            fused_scores[key] += alpha * score

            dense_lookup[key] = result

        for result, score in zip(
            sparse_response.results,
            sparse_norm,
        ):

            key = self.get_chunk_key(result)

            fused_scores[key] += (1 - alpha) * score

            sparse_lookup[key] = result

        ranked = sorted(
            fused_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        ranked = ranked[: self.k]

        retrieval_results = []

        for rank, (key, hybrid_score) in enumerate(
            ranked,
            start=1,
        ):

            if key in dense_lookup:
                result = dense_lookup[key]
            else:
                result = sparse_lookup[key]

            retrieval_results.append(
                RetrievalResult(
                    rank=rank,
                    retrieval_score=float(hybrid_score),
                    score_type=HYBRID_SCORE,
                    retriever=HYBRID_RETRIEVER,
                    document=result.document,
                )
            )

        return RetrievalResponse(
            query=query,
            retriever=HYBRID_RETRIEVER,
            latency=0.0,
            results=retrieval_results,
        )

    def search_with_scores(
        self,
        query: str,
        alpha: float = 0.5,
    ) -> RetrievalResponse:

        start = time.perf_counter()

        dense_response = self.dense_search(query)

        sparse_response = self.sparse_search(query)

        response = self.fuse_results(
            query=query,
            dense_response=dense_response,
            sparse_response=sparse_response,
            alpha=alpha,
        )

        response.latency = time.perf_counter() - start

        return response

    def summary(self):

        print("\n")
        print(" HYBRID RETRIEVER SUMMARY ".center(70, "="))
        print(f"Top K          : {self.k}")
        print(f"Fusion Method  : Weighted Score Fusion")
        print("=" * 70)
