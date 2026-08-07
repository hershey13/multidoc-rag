from src.retrievers.schemas import RetrievalResponse


def display_results(
    response: RetrievalResponse,
    preview_length: int = 400,
) -> None:
    """
    Pretty-print retrieval results for any retriever.

    Works with:
    - Dense Retriever
    - Sparse Retriever
    - Hybrid Retriever
    """

    print("\n")
    print(f" {response.retriever.upper()} RETRIEVAL RESULTS ".center(90, "="))

    print(f"Query      : {response.query}")
    print(f"Retriever  : {response.retriever}")
    print(f"Latency    : {response.latency:.3f} seconds")

    print("=" * 90)

    for result in response.results:

        doc = result.document

        print()

        print(f"Rank       : {result.rank}")
        print(f"Score Type : {result.score_type}")
        print(f"Score      : {result.retrieval_score:.4f}")

        print(f"File       : {doc.metadata.get('filename')}")
        print(f"Category   : {doc.metadata.get('category')}")
        print(f"Chunk ID   : {doc.metadata.get('chunk_id')}")

        if "page" in doc.metadata:
            print(f"Page       : {doc.metadata['page'] + 1}")

        print("-" * 90)

        preview = doc.page_content.strip()

        if len(preview) > preview_length:
            preview = preview[:preview_length] + "..."

        print(preview)

        print("=" * 90)
