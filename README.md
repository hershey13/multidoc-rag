Multi-Document Question Answering using Retrieval-Augmented Generation (RAG)
This project presents a Retrieval-Augmented Generation (RAG) based Multi-Document Question Answering system that generates accurate, context-aware responses from a large collection of enterprise documents.
The system preprocesses documents using recursive chunking, creates dense vector embeddings, and stores them in ChromaDB for efficient retrieval. To improve retrieval quality, Dense Retrieval, Hybrid Retrieval (BM25 + Dense + Reciprocal Rank Fusion), and Cross-Encoder reranking were implemented and evaluated.
Performance was assessed using retrieval metrics (Precision@5, Recall@5, MRR, MAP, nDCG@5) and RAGAS metrics (Faithfulness, Answer Relevancy, Context Precision, and Context Recall).
A Streamlit-based interface enables users to interact with the system, view grounded answers, and access source citations. The results demonstrate that the proposed retrieval pipeline significantly improves the relevance and reliability of responses for multi-document question answering.


The project is deployed using:
Frontend: Streamlit
Backend: Azure App Service
Containerization: Docker

⚙️Installation

Clone the repository:

git clone <repository-url>

Move into the project directory:

cd <repository-name>

Create a virtual environment:

python -m venv .venv

Activate the environment:

Windows
.venv\Scripts\activate

▶️Running the Backend
uvicorn app.main:app --reload
▶️ Running the Frontend
streamlit run app.py
▶️ Docker
Build the Docker image:
docker build -t multidoc-rag .
