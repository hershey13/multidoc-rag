from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from rag_pipeline import RAGPipeline
from models import QueryRequest, QueryResponse

app = FastAPI(
    title="Multi-Document RAG API",
    version="1.0.0",
)

# Allow Streamlit to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # we'll restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("=" * 70)
print("Loading RAG Pipeline...")
print("=" * 70)

pipeline = RAGPipeline(retriever_type="hybrid_rrf")

print("=" * 70)
print("Pipeline Ready!")
print("=" * 70)


@app.get("/")
def root():
    return {
        "status": "running",
        "project": "Multi-Document RAG",
    }


@app.post(
    "/query",
    response_model=QueryResponse,
)
def query(request: QueryRequest):

    result = pipeline.ask(request.question)

    return QueryResponse(**result)
