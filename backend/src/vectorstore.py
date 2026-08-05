from pathlib import Path
from typing import List
import shutil

from tqdm import tqdm
from langchain_core.documents import Document
from langchain_chroma import Chroma

from src.embeddings import get_embedding_model

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

DEFAULT_COLLECTION_NAME = "multidoc_rag"
DEFAULT_DB_PATH = "./chroma_db"


# ------------------------------------------------------------------
# Create / Load Vector Store
# ------------------------------------------------------------------


def create_vectorstore(
    persist_directory: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
    reset_db: bool = False,
) -> Chroma:
    """
    Create a persistent ChromaDB vector store.

    Parameters
    ----------
    persist_directory : str
        Directory where ChromaDB is stored.

    collection_name : str
        Name of the Chroma collection.

    reset_db : bool
        Delete the existing database before creating a new one.
    """

    db_path = Path(persist_directory)

    if reset_db and db_path.exists():
        print("Removing existing Chroma database...")
        shutil.rmtree(db_path)

    embedding_model = get_embedding_model()

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=persist_directory,
    )

    return vectorstore


def load_vectorstore(
    persist_directory: str = DEFAULT_DB_PATH,
    collection_name: str = DEFAULT_COLLECTION_NAME,
) -> Chroma:
    """
    Load an existing persistent ChromaDB vector store.
    """

    embedding_model = get_embedding_model()

    vectorstore = Chroma(
        collection_name=collection_name,
        embedding_function=embedding_model,
        persist_directory=persist_directory,
    )

    return vectorstore


# ------------------------------------------------------------------
# Index Documents
# ------------------------------------------------------------------
def get_existing_ids(
    vectorstore: Chroma,
) -> set[str]:
    """
    Return all document IDs currently stored in ChromaDB.
    """

    data = vectorstore.get(include=[])

    return set(data["ids"])


def index_documents(
    vectorstore: Chroma,
    documents: List[Document],
    batch_size: int = 500,
):
    """
    Incrementally index documents into ChromaDB.

    Existing chunks are skipped.
    Only new chunks are embedded and stored.
    """

    total_documents = len(documents)

    existing_ids = get_existing_ids(vectorstore)

    added = 0
    skipped = 0

    print(f"Already indexed : {len(existing_ids)}")
    print(f"\nProcessing {total_documents} chunks...\n")

    for start in tqdm(
        range(0, total_documents, batch_size),
        desc="Embedding & Indexing",
    ):

        end = min(start + batch_size, total_documents)

        batch = []
        ids = []

        for doc in documents[start:end]:

            doc_id = f"{doc.metadata['doc_id']}_chunk_{doc.metadata['chunk_id']}"

            if doc_id in existing_ids:
                skipped += 1
                continue

            batch.append(doc)
            ids.append(doc_id)

        # Skip empty batches
        if not batch:
            continue

        vectorstore.add_documents(
            documents=batch,
            ids=ids,
        )

        # Update counters
        added += len(batch)

        # Prevent duplicates during the same run
        existing_ids.update(ids)

    print("\nIndexing Complete!")
    print(f"Added chunks   : {added}")
    print(f"Skipped chunks : {skipped}")
    print(f"Total in DB    : {count_documents(vectorstore)}")


# ------------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------------


def count_documents(vectorstore: Chroma) -> int:
    """
    Return number of indexed chunks.
    """

    try:
        return vectorstore._collection.count()
    except Exception:
        return 0


def delete_vectorstore(
    persist_directory: str = DEFAULT_DB_PATH,
):
    """
    Delete the existing Chroma database.
    """

    db_path = Path(persist_directory)

    if db_path.exists():
        shutil.rmtree(db_path)
        print("Vector store deleted.")
    else:
        print("Vector store does not exist.")
