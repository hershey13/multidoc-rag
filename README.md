# Multi-Document Question Answering with RAG

## Table of Contents

* [Introduction](#introduction)
* [Key Features](#key-features)
* [Technology Stack](#technology-stack)
* [Dataset and Knowledge Base](#dataset-and-knowledge-base)
* [RAG Pipeline Overview](#rag-pipeline-overview)
* [Document Processing and Chunking](#document-processing-and-chunking)
* [Embedding and Vector Database](#embedding-and-vector-database)
* [Retrieval Strategies](#retrieval-strategies)
* [Reranking with Cross-Encoder](#reranking-with-cross-encoder)
* [Multi-Hop Question Answering](#multi-hop-question-answering)
* [Evaluation and Metrics](#evaluation-and-metrics)
* [System Architecture](#system-architecture)
* [File Structure](#file-structure)
* [Installation and How to Use](#installation-and-how-to-use)
* [Deployment](#deployment)
* [Future Improvements](#future-improvements)
* [Acknowledgements](#acknowledgements)

## Introduction

This project implements a **Multi-Document Question Answering system using Retrieval-Augmented Generation (RAG)**. The system enables users to ask questions across a large collection of documents and generates grounded answers using relevant information retrieved from the knowledge base.

The project focuses on improving the reliability and relevance of document-based question answering by combining **dense vector retrieval, sparse BM25 retrieval, Reciprocal Rank Fusion (RRF), and Cross-Encoder reranking**.

The system processes documents through a complete RAG pipeline, including document loading, text extraction, chunking, embedding generation, vector indexing, retrieval, reranking, and response generation.

The knowledge base contains over **1,000 documents**, including Markdown and PDF content, and is designed to handle questions involving shared entities, overlapping topics, and cross-document dependencies.

The project also evaluates different retrieval configurations using metrics such as **Precision@K, Recall@K, MRR, nDCG, MAP, and RAGAS-based evaluation metrics** to compare retrieval and answer quality.

## Key Features

* Multi-document question answering using RAG
* Support for Markdown and PDF documents
* Document preprocessing and text extraction
* Recursive and semantic chunking strategies
* Configurable chunk size and overlap
* Dense vector retrieval
* Sparse BM25 retrieval
* Hybrid retrieval using Dense + BM25
* Reciprocal Rank Fusion (RRF)
* Cross-Encoder based reranking
* Metadata-aware document retrieval
* Multi-hop question answering
* Source-grounded responses
* Retrieval performance evaluation
* RAGAS-based answer evaluation
* FastAPI backend
* Streamlit-based frontend
* Docker-based deployment
* Azure cloud deployment

## Technology Stack

| Component            | Technology             |
| -------------------- | ---------------------- |
| Programming Language | Python                 |
| Backend              | FastAPI                |
| Frontend             | Streamlit              |
| LLM                  | Gemini                 |
| Embeddings           | BAAI/bge-small-en-v1.5 |
| Vector Database      | ChromaDB               |
| Sparse Retrieval     | BM25                   |
| Hybrid Retrieval     | RRF                    |
| Reranking            | Cross-Encoder          |
| Containerization     | Docker                 |
| Cloud Platform       | Microsoft Azure        |
| Evaluation           | RAGAS, NDCG, MAP, MRR  |
| Version Control      | Git and GitHub         |

## Dataset and Knowledge Base

The system was developed using a multi-document knowledge base containing approximately **1,063 documents**.

The dataset consists of:

* 1,027 Markdown documents
* 36 PDF pages
* More than 28,000 generated text chunks

The documents contain overlapping information and shared entities, allowing the system to be evaluated on both straightforward questions and questions requiring information from multiple documents.

### Dataset Statistics

| Property             |  Value |
| -------------------- | -----: |
| Total Documents      |  1,063 |
| Markdown Documents   |  1,027 |
| PDF Pages            |     36 |
| Generated Chunks     | 28,346 |
| Maximum Chunk Length |    500 |
| Average Chunk Length | 336.70 |
| Minimum Chunk Length |     50 |

## RAG Pipeline Overview

The system follows the following retrieval-augmented generation pipeline:

```text
User Query
    |
    v
Query Processing
    |
    v
Document Retrieval
    |
    +----------------------+
    |                      |
    v                      v
Dense Retrieval       BM25 Retrieval
    |                      |
    +----------+-----------+
               |
               v
       Reciprocal Rank Fusion
               |
               v
       Candidate Documents
               |
               v
       Cross-Encoder Reranking
               |
               v
        Top-K Relevant Chunks
               |
               v
       Context Construction
               |
               v
          LLM Generation
               |
               v
       Grounded Answer
```

The pipeline combines multiple retrieval approaches to improve both semantic relevance and keyword-level matching.

## Document Processing and Chunking

Documents are first loaded and converted into a standardized text representation. The extracted content is then divided into smaller chunks before embedding.

Different chunking configurations were experimented with to determine their effect on retrieval performance.

The experiments included:

* Recursive chunking
* Semantic chunking
* Different chunk sizes
* Different chunk overlaps
* Different embedding models

Chunking experiments were evaluated using retrieval metrics such as **MRR, MAP, nDCG, Precision@K, and Recall@K**.

## Embedding and Vector Database

The project uses the **BAAI/bge-small-en-v1.5** embedding model to convert document chunks into dense vector representations.

The generated embeddings are stored in **ChromaDB**, which provides persistent vector storage and similarity search.

The embedding configuration uses normalized embeddings and CPU-based inference.

```text
Documents
    |
    v
Text Chunks
    |
    v
BGE Embedding Model
    |
    v
Dense Vector Representations
    |
    v
ChromaDB
```

## Retrieval Strategies

Multiple retrieval strategies were implemented and compared.

### Dense Retrieval

Dense retrieval uses vector embeddings to identify documents that are semantically similar to the user query.

### BM25 Retrieval

BM25 provides sparse keyword-based retrieval and is particularly useful for exact terms, names, identifiers, and domain-specific terminology.

### Hybrid Retrieval

Hybrid retrieval combines dense and sparse retrieval to leverage both semantic and lexical matching.

```text
                    User Query
                        |
             +----------+----------+
             |                     |
             v                     v
       Dense Retrieval        BM25 Retrieval
             |                     |
             +----------+----------+
                        |
                        v
                Reciprocal Rank
                    Fusion
                        |
                        v
                Combined Ranking
```

## Reranking with Cross-Encoder

After the initial retrieval stage, candidate chunks are passed through a **Cross-Encoder** for more precise relevance scoring.

Unlike independent embedding-based retrieval, a Cross-Encoder evaluates the query and candidate document together, allowing it to model their interaction more directly.

The final pipeline therefore follows:

```text
Query
  |
  v
Dense + BM25 Retrieval
  |
  v
RRF Fusion
  |
  v
Candidate Chunks
  |
  v
Cross-Encoder Reranking
  |
  v
Top-K Context
```

This approach was evaluated against standalone dense and hybrid retrieval configurations.

## Multi-Hop Question Answering

The system also includes evaluation of **multi-hop questions**, where answering a query requires combining information from multiple pieces of retrieved context.

For example:

> How are employee expenses reimbursed and how are they reflected in payroll?

Such questions require the system to retrieve relevant information about both **expense reimbursement** and **payroll processing**, potentially from different documents.

Multi-hop evaluation was used to test the system's ability to retrieve complementary information rather than relying on a single highly similar document.

## Evaluation and Metrics

The retrieval pipeline was evaluated using multiple information retrieval metrics.

### Retrieval Metrics

* Precision@5
* Recall@5
* Mean Reciprocal Rank (MRR)
* Normalized Discounted Cumulative Gain (nDCG@5)
* Mean Average Precision (MAP)

### Answer Evaluation

RAGAS-based evaluation was used to assess generated responses using metrics such as:

* Faithfulness
* Answer Relevancy
* Context Relevancy
* Context Recall

Different combinations of chunking strategies, embedding models, and retrieval methods were compared to identify configurations that provided better retrieval and answer quality.

## System Architecture

The system consists of three primary layers:

### Frontend

The user interface is implemented using **Streamlit**, allowing users to enter questions and interact with the RAG system.

### Backend

The backend is implemented using **FastAPI** and handles:

* Query processing
* Document retrieval
* Context preparation
* LLM interaction
* Response generation
* API endpoints

### Retrieval and Knowledge Layer

The retrieval layer consists of:

* ChromaDB
* Dense embeddings
* BM25
* Reciprocal Rank Fusion
* Cross-Encoder reranking

```text
                Streamlit Frontend
                        |
                        v
                  FastAPI Backend
                        |
                        v
                 Query Processing
                        |
              +---------+---------+
              |                   |
              v                   v
        Dense Retrieval       BM25 Retrieval
              |                   |
              +---------+---------+
                        |
                        v
                    RRF Fusion
                        |
                        v
               Cross-Encoder
                  Reranking
                        |
                        v
                   Top-K Context
                        |
                        v
                     Gemini
                        |
                        v
                 Final Answer
```

## File Structure

```text
Multi-Doc-RAG/
│
├── backend/
│   ├── app/
│   ├── data/
│   ├── experiments/
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── ...
│
├── frontend/
│   ├── app.py
│   └── ...
│
├── experiments/
│   ├── ground_truth.csv
│   ├── retrieval_results.csv
│   ├── metrics.csv
│   └── ...
│
├── README.md
└── .gitignore
```

## Installation and How to Use

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Multi-Doc-RAG
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

```bash
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file and configure the required API keys and application settings.

```env
GEMINI_API_KEY=your_api_key
CHROMA_DB_PATH=./chroma_db
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K=4
```

### 5. Run the Backend

```bash
uvicorn app.main:app --reload
```

The FastAPI documentation can then be accessed through the `/docs` endpoint.

### 6. Run the Frontend

```bash
streamlit run app.py
```

The Streamlit interface can then be used to submit questions to the RAG system.

## Deployment

The application is containerized using **Docker** and deployed on **Microsoft Azure**.

The deployment architecture consists of:

```text
                User
                 |
                 v
        Streamlit Frontend
                 |
                 v
          Azure Deployment
                 |
                 v
          Docker Container
                 |
                 v
          FastAPI Backend
                 |
        +--------+--------+
        |                 |
        v                 v
     ChromaDB          Gemini API
```

## Future Improvements

* Improve multi-hop retrieval and reasoning
* Add query decomposition for complex questions
* Experiment with larger and domain-specific embedding models
* Implement adaptive chunking
* Improve metadata-based filtering
* Optimize retrieval latency
* Add conversation memory
* Improve citation and source visualization
* Evaluate additional reranking models
* Expand automated RAGAS evaluation
* Add authentication and access control
* Improve scalability for larger document collections

## Acknowledgements

This project was developed as part of an internship project focused on **Generative AI, Retrieval-Augmented Generation, information retrieval, and multi-document question answering**.

The project benefited from open-source libraries and frameworks including **FastAPI, Streamlit, ChromaDB, LangChain, Hugging Face, RAGAS, and Google Gemini**.
