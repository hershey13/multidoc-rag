import time
from typing import List

from langchain_core.documents import Document

from src.config import (
    TOP_K,
    SEARCH_TYPE,
    DENSE_RETRIEVER,
    COSINE_DISTANCE,
)
from src.vectorstore import load_vectorstore
from src.retrievers.schemas import (
    RetrievalResult,
    RetrievalResponse,
)


class DenseRetriever:
    """
    Dense retriever backed by ChromaDB.
    """

    def __init__(
        self,
        k: int = TOP_K,
        search_type: str = SEARCH_TYPE,
        persist_directory: str | None = None,
    ):
        """
        Initialize the dense retriever.
        """

        self.k = k
        self.search_type = search_type

        # Load the requested Chroma database
        if persist_directory is None:
            self.vectorstore = load_vectorstore()
        else:
            self.vectorstore = load_vectorstore(
                persist_directory=persist_directory,
            )

        # LangChain retriever interface
        self.index = self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={
                "k": self.k,
            },
        )

    # --------------------------------------------------------------
    # Search
    # --------------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> List[Document]:
        """
        Retrieve the top-k documents.
        """

        return self.index.invoke(query)

    # --------------------------------------------------------------
    # Search With Scores
    # --------------------------------------------------------------

    def search_with_scores(
        self,
        query: str,
        metadata_filter: dict | None = None,
    ) -> RetrievalResponse:
        """
        Retrieve the top-k documents together with
        similarity scores.
        """

        start = time.perf_counter()

        results = self.vectorstore.similarity_search_with_score(
            query=query,
            k=self.k,
            filter=metadata_filter,
        )

        latency = time.perf_counter() - start

        retrieval_results: List[RetrievalResult] = []

        for rank, (doc, distance) in enumerate(
            results,
            start=1,
        ):

            retrieval_results.append(
                RetrievalResult(
                    rank=rank,
                    retrieval_score=float(distance),
                    score_type=COSINE_DISTANCE,
                    retriever=DENSE_RETRIEVER,
                    document=doc,
                )
            )

        return RetrievalResponse(
            query=query,
            retriever=DENSE_RETRIEVER,
            latency=latency,
            results=retrieval_results,
        )

    # --------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------

    def summary(self) -> None:
        """
        Display information about the dense retriever.
        """

        print("\n")
        print(" DENSE RETRIEVER SUMMARY ".center(70, "="))

        print(f"Search Type : {self.search_type}")
        print(f"Top K       : {self.k}")

        print("=" * 70)
