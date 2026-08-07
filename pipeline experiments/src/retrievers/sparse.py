from __future__ import annotations

import re
import time
from typing import List

import numpy as np
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi

from src.config import (
    TOP_K,
    SPARSE_RETRIEVER,
    BM25_SCORE,
)
from src.retrievers.schemas import (
    RetrievalResult,
    RetrievalResponse,
)

# ------------------------------------------------------------------
# Tokenizer
# ------------------------------------------------------------------


def tokenize(text: str) -> List[str]:
    """
    Tokenize text for BM25 retrieval.

    - Convert to lowercase
    - Extract alphanumeric words.
    """

    return re.findall(r"\b\w+\b", text.lower())


# ------------------------------------------------------------------
# Sparse Retriever
# ------------------------------------------------------------------


class SparseRetriever:
    """
    BM25-based sparse retriever.
    """

    def __init__(
        self,
        documents: List[Document],
    ):

        self.documents = documents

        self.tokenized_corpus = [tokenize(doc.page_content) for doc in documents]

        self.index = BM25Okapi(self.tokenized_corpus)

    # --------------------------------------------------------------
    # Search
    # --------------------------------------------------------------

    def search(
        self,
        query: str,
        k: int = TOP_K,
    ) -> List[Document]:
        """
        Retrieve the top-k most relevant documents.
        """

        query_tokens = tokenize(query)

        scores = self.index.get_scores(query_tokens)

        ranked_indices = np.argsort(scores)[::-1][:k]

        return [self.documents[idx] for idx in ranked_indices]

    # --------------------------------------------------------------
    # Search With Scores
    # --------------------------------------------------------------

    def search_with_scores(
        self,
        query: str,
        k: int = TOP_K,
    ) -> RetrievalResponse:
        """
        Retrieve the top-k documents together with BM25 scores.
        """

        start = time.perf_counter()

        query_tokens = tokenize(query)

        scores = self.index.get_scores(query_tokens)

        ranked_indices = np.argsort(scores)[::-1][:k]

        latency = time.perf_counter() - start

        retrieval_results: List[RetrievalResult] = []

        for rank, idx in enumerate(
            ranked_indices,
            start=1,
        ):

            retrieval_results.append(
                RetrievalResult(
                    rank=rank,
                    retrieval_score=float(scores[idx]),
                    score_type=BM25_SCORE,
                    retriever=SPARSE_RETRIEVER,
                    document=self.documents[idx],
                )
            )

        return RetrievalResponse(
            query=query,
            retriever=SPARSE_RETRIEVER,
            latency=latency,
            results=retrieval_results,
        )

    # --------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------

    def summary(self) -> None:
        """
        Display information about the BM25 index.
        """

        print("\n")
        print(" SPARSE RETRIEVER SUMMARY ".center(70, "="))

        print(f"Documents          : {len(self.documents)}")
        print(f"Tokenized Docs     : {len(self.tokenized_corpus)}")
        print(f"Vocabulary Size    : {len(self.index.idf)}")
        print(f"Average Doc Length : {self.index.avgdl:.2f}")

        print("=" * 70)

    # ------------------------------------------------------------------
    # Display Results
    # ------------------------------------------------------------------
    #
