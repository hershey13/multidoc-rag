def print_retrieval_summary(
    response,
):
    print("\nRetrieval Summary")
    print("-" * 50)

    print(f"Retriever : {response.retriever}")
    print(f"Latency   : {response.latency:.3f} s")
    print(f"Results   : {len(response.results)}")

    categories = {
        result.document.metadata.get("category") for result in response.results
    }

    print(f"Categories: {sorted(categories)}")
