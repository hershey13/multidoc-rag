from dataclasses import dataclass
from typing import List
import time

from langchain_core.documents import Document

from src.vectorstore import load_vectorstore
from src.config import TOP_K, SEARCH_TYPE


@dataclass
class RetrievalResult:
    """
    Represents one retrieved document.
    """

    rank: int
    score: float
    document: Document
    retriever: str = "Dense"


def load_dense_retriever(
    k: int = TOP_K,
):
    """
    Load the Chroma dense retriever.
    """

    vectorstore = load_vectorstore()

    return vectorstore.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={"k": k},
    )


def retrieve_documents(
    query: str,
    k: int = TOP_K,
    metadata_filter: dict | None = None,
):
    """
    Retrieve top-k relevant documents.
    """

    vectorstore = load_vectorstore()

    start = time.perf_counter()

    results = vectorstore.similarity_search_with_score(
        query=query,
        k=k,
        filter=metadata_filter,
    )

    elapsed = time.perf_counter() - start

    retrieval_results = []

    for rank, (doc, score) in enumerate(results, start=1):

        retrieval_results.append(
            RetrievalResult(
                rank=rank,
                score=float(score),
                document=doc,
                retriever="Dense",
            )
        )

    return retrieval_results, elapsed


def display_results(results):
    """
    Pretty print retrieved documents.
    """

    for result in results:

        doc = result.document

        print("=" * 80)

        print(f"Rank      : {result.rank}")

        print(f"Score     : {result.score:.4f}")

        print(f"Retriever : {result.retriever}")

        print(f"File      : {doc.metadata.get('filename')}")

        print(f"Category  : {doc.metadata.get('category')}")

        if "page" in doc.metadata:

            print(f"Page      : {doc.metadata['page'] + 1}")

        print("-" * 80)

        print(doc.page_content[:400])

        print()
