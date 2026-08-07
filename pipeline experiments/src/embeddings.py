from langchain_huggingface import HuggingFaceEmbeddings


def get_embedding_model(
    model_name: str = "BAAI/bge-small-en-v1.5",
):
    """
    Load the embedding model.
    """

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    return embeddings


# BAAI/bge-base-en-v1.5
