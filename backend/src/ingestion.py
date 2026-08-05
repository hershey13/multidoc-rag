from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
)


def add_metadata(
    doc: Document,
    file_path: Path,
    root_dir: Path,
    file_type: str,
) -> None:
    """
    Add standardized metadata to a document.
    """

    doc.metadata["file_type"] = file_type
    doc.metadata["filename"] = file_path.name
    doc.metadata["category"] = file_path.parent.name
    doc.metadata["relative_path"] = file_path.relative_to(root_dir).as_posix()
    doc.metadata["doc_id"] = f"{file_path.parent.name}/{file_path.name}"


def load_pdfs(pdf_directory: str) -> List[Document]:
    """
    Load all PDF files recursively from a directory.
    Each PDF page becomes one LangChain Document.
    """

    pdf_dir = Path(pdf_directory)
    pdf_files = sorted(pdf_dir.rglob("*.pdf"))

    all_documents: List[Document] = []

    print(f"Found {len(pdf_files)} PDF files.")

    for pdf_file in pdf_files:

        try:
            loader = PyMuPDFLoader(str(pdf_file))
            documents = loader.load()

            for doc in documents:
                add_metadata(
                    doc,
                    pdf_file,
                    pdf_dir,
                    "pdf",
                )

            all_documents.extend(documents)

        except Exception as e:
            print(f"Failed to load {pdf_file.name}: {e}")

    print(f"Loaded {len(all_documents)} PDF pages.\n")

    return all_documents


from pathlib import Path


def load_markdown(md_directory: str) -> List[Document]:
    """
    Load all Markdown files recursively.
    """

    md_dir = Path(md_directory)
    md_files = sorted(md_dir.rglob("*.md"))

    all_documents: List[Document] = []

    print(f"Found {len(md_files)} Markdown files.")

    for md_file in md_files:

        try:
            loader = TextLoader(
                str(md_file),
                encoding="utf-8",
                autodetect_encoding=True,
            )

            documents = loader.load()

            for doc in documents:
                add_metadata(
                    doc,
                    md_file,
                    md_dir,
                    "markdown",
                )

            all_documents.extend(documents)

        except Exception as e:
            print(f"Failed to load {md_file.name}: {e}")

    print(f"Loaded {len(all_documents)} Markdown documents.\n")

    return all_documents


def load_documents(data_directory: str) -> List[Document]:
    """
    Load every supported document type from the corpus.
    """

    pdf_docs = load_pdfs(data_directory)
    md_docs = load_markdown(data_directory)

    all_docs = pdf_docs + md_docs

    print("=" * 50)
    print(f"Total documents loaded: {len(all_docs)}")
    print("=" * 50)

    return all_docs
