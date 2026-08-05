from config import DATA_DIR, VECTOR_DB_PATH

from src.ingestion import load_documents
from src.chunking import split_documents

from src.retrievers.dense import DenseRetriever
from src.retrievers.hybrid import HybridRetriever
from src.retrievers.hybrid_rrf import HybridRRFRetriever

from generator import generate

from pathlib import Path

# print("Current Working Directory:", Path.cwd())


class RAGPipeline:

    def __init__(
        self,
        retriever_type="hybrid_rrf",
    ):

        print("=" * 70)
        print("Initializing RAG Pipeline...")
        print("=" * 70)

        self.retriever_type = retriever_type

        # ---------------------------------------------------
        # Debug
        # ---------------------------------------------------

        # print("\n===== DATA DIRECTORY DEBUG =====")
        # print("DATA_DIR:", DATA_DIR)
        # print("Exists:", DATA_DIR.exists())

        # for item in DATA_DIR.iterdir():
        #     print(item)

        # print("===============================\n")

        # ---------------------------------------------------
        # Load Documents
        # ---------------------------------------------------

        self.documents = load_documents(str(DATA_DIR))

        print(f"Documents Loaded: {len(self.documents)}")

        # ---------------------------------------------------
        # Chunk Documents
        # ---------------------------------------------------

        self.chunks = split_documents(
            self.documents,
            chunk_size=700,
            chunk_overlap=100,
            chunking_method="recursive",
        )

        print(f"Chunks Created: {len(self.chunks)}")

        # ---------------------------------------------------
        # Load Retriever
        # ---------------------------------------------------

        if retriever_type == "dense":

            self.retriever = DenseRetriever(
                persist_directory=str(VECTOR_DB_PATH),
            )

        elif retriever_type == "hybrid":

            self.retriever = HybridRetriever(
                chunks=self.chunks,
                persist_directory=str(VECTOR_DB_PATH),
            )

        elif retriever_type == "hybrid_rrf":

            self.retriever = HybridRRFRetriever(
                chunks=self.chunks,
                persist_directory=str(VECTOR_DB_PATH),
            )

        else:

            raise ValueError(f"Unknown retriever: {retriever_type}")

        print("Retriever Loaded")
        print("=" * 70)

    # --------------------------------------------------------
    # Ask Question
    # --------------------------------------------------------

    def ask(self, question):

        retrieval_response = self.retriever.search_with_scores(question)

        generation = generate(
            question,
            retrieval_response.results,
        )

        sources = []

        for result in retrieval_response.results:

            doc = result.document

            sources.append(
                {
                    "rank": result.rank,
                    "score": round(result.retrieval_score, 4),
                    "file_name": doc.metadata.get(
                        "filename",
                        "Unknown",
                    ),
                    "page": doc.metadata.get("page"),
                    "category": doc.metadata.get("category"),
                    "chunk_id": doc.metadata.get("chunk_id"),
                    "preview": doc.page_content[:300],
                }
            )

        return {
            "answer": generation["answer"],
            "contexts": generation["contexts"],
            "sources": sources,
            "retriever": retrieval_response.retriever,
            "latency": retrieval_response.latency,
        }
