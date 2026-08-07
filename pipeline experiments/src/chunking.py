# from typing import List

# from langchain_core.documents import Document
# from langchain_text_splitters import RecursiveCharacterTextSplitter


# def create_text_splitter(
#     chunk_size: int,  # baseline 500
#     chunk_overlap: int,  # baseline 100
# ) -> RecursiveCharacterTextSplitter:
#     """
#     Create a RecursiveCharacterTextSplitter optimized for
#     Markdown and PDF documents.
#     """

#     return RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#         length_function=len,
#         separators=[
#             "\n# ",
#             "\n## ",
#             "\n### ",
#             "\n\n",
#             "\n",
#             ". ",
#             " ",
#             "",
#         ],
#     )


# def split_documents(
#     documents,
#     chunk_size,
#     chunk_overlap,
# ):
#     splitter = create_text_splitter(
#         chunk_size=chunk_size,
#         chunk_overlap=chunk_overlap,
#     )

#     chunks = splitter.split_documents(documents)

#     # Remove tiny chunks
#     chunks = [chunk for chunk in chunks if len(chunk.page_content.strip()) >= 50]

#     # Assign chunk IDs
#     for idx, chunk in enumerate(chunks):
#         chunk.metadata["chunk_id"] = idx

#     return chunks

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)

from langchain_experimental.text_splitter import SemanticChunker
from src.embeddings import get_embedding_model


def create_recursive_splitter(
    chunk_size: int,
    chunk_overlap: int,
):

    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=[
            "\n# ",
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )


def create_markdown_splitter():

    headers = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    return MarkdownHeaderTextSplitter(
        headers_to_split_on=headers,
        strip_headers=False,
    )


def create_semantic_splitter():

    embedding_model = get_embedding_model()

    return SemanticChunker(
        embedding_model,
    )


def split_documents(
    documents,
    chunk_size=700,
    chunk_overlap=100,
    chunking_method="recursive",
):

    if chunking_method == "recursive":

        splitter = create_recursive_splitter(
            chunk_size,
            chunk_overlap,
        )

        chunks = splitter.split_documents(documents)

    elif chunking_method == "markdown":

        splitter = create_markdown_splitter()

        chunks = []

        for doc in documents:

            # Markdown splitter expects text
            md_chunks = splitter.split_text(doc.page_content)

            for chunk in md_chunks:

                chunk.metadata.update(doc.metadata)

                chunks.append(chunk)

    elif chunking_method == "semantic":

        splitter = create_semantic_splitter()

        chunks = splitter.split_documents(documents)

    else:

        raise ValueError(f"Unknown chunking method: {chunking_method}")
    chunks = [chunk for chunk in chunks if len(chunk.page_content.strip()) >= 50]

    for idx, chunk in enumerate(chunks):

        chunk.metadata["chunk_id"] = idx

    return chunks
