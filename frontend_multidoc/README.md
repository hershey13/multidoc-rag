# Multi-Document Question Answering using RAG

A Retrieval-Augmented Generation (RAG) based Multi-Document Question Answering system that retrieves relevant information from enterprise documents and generates grounded, context-aware responses with source citations.

## Features

- Multi-document semantic search
- Dense Retrieval using ChromaDB
- Hybrid Retrieval (BM25 + Dense + Reciprocal Rank Fusion)
- Cross-Encoder Re-ranking
- Source citations
- Streamlit-based user interface
- FastAPI backend
- Evaluation using RAGAS and Information Retrieval metrics

## Tech Stack

- Python 3.11
- FastAPI
- Streamlit
- LangChain
- ChromaDB
- HuggingFace Embeddings (BAAI/bge-small-en-v1.5)
- Groq API
- RAGAS
- BM25
- Cross Encoder

---

## Project Structure

```
multidoc-rag/
│
├── frontend/
│   └── app.py
│
├── src/
│   ├── api.py
│   ├── retrievers/
│   ├── ingestion.py
│   ├── chunking.py
│   ├── embeddings.py
│   └── vectorstore.py
│
├── chroma_db/
├── data/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/multidoc-rag.git
```

Move into the project

```bash
cd multidoc-rag
```

Create a virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=YOUR_API_KEY
```

---

## Running the Backend

```bash
 uvicorn main:app --reload
```

Backend runs on

```
http://127.0.0.1:8000
```

---

## Running the Frontend

```bash
streamlit run frontend/app.py
```

Frontend runs on

```
http://localhost:8501
```

---

## Evaluation

The project was evaluated using:

### Retrieval Metrics

- Precision@5
- Recall@5
- MRR
- MAP
- nDCG@5

### RAGAS Metrics

- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall

---

## Dataset

GitLab Documentation

https://gitlab.com/gitlab-org/gitlab/-/tree/master/doc

GitLab Handbook

https://handbook.gitlab.com/

---
