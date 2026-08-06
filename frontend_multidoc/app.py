"""
Multi-Document Question Answering
Retrieval-Augmented Generation for Document Intelligence

A minimal, premium single-page Streamlit application for a RAG-based
multi-document QA system. No sidebar — a focused, elegant landing page
centered on a single question-and-answer experience. Fully functional
with dummy data and structured so a real RAG backend can be connected later.

Backend integration points (currently placeholders):
    - retrieve_documents()
    - rerank_results()
    - generate_answer()
    - display_sources()
"""

import time
import random
import requests
from datetime import datetime
from textwrap import dedent
import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Document Question Answering",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------------------------
# Fixed configuration (previously the sidebar controls)
# ---------------------------------------------------------------------------
CONFIG = {
    "method": "Hybrid + Cross Encoder",
    "embedding_model": "BAAI/bge-small-en-v1.5",
    "chunk_size": 500,
    "top_k": 5,
}


# ---------------------------------------------------------------------------
# Custom CSS  --  overrides Streamlit defaults for a premium, minimal look
# ---------------------------------------------------------------------------
def inject_css() -> None:
    st.markdown(
        """
        <style>
        /* ----- Fonts ----- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }

        /* ----- Color tokens ----- */
        :root {
            --bg: #FAFAF9;
            --card: #FFFFFF;
            --text-primary: #18181B;
            --text-secondary: #71717A;
            --accent: #2563EB;
            --accent-soft: rgba(37, 99, 235, 0.08);
            --border: #EAEAE7;
        }

        /* ----- App background ----- */
        .stApp {
            background:
                radial-gradient(1200px 500px at 50% -10%, rgba(37,99,235,0.05), transparent 70%),
                var(--bg);
        }

        .block-container {
            padding-top: 4.5rem;
            padding-bottom: 5rem;
            max-width: 760px;
        }

        /* ----- Hero ----- */
        .eyebrow {
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            color: var(--accent);
            background: var(--accent-soft);
            border-radius: 999px;
            padding: 0.35rem 0.85rem;
            margin-bottom: 1.5rem;
        }
        .page-title {
            font-family: 'Fraunces', Georgia, serif;
            font-size: 3.4rem;
            line-height: 1.05;
            font-weight: 500;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            margin-bottom: 1rem;
            text-wrap: balance;
        }
        .page-title em {
            font-style: italic;
            color: var(--accent);
        }
        .page-subtitle {
            font-size: 1.12rem;
            line-height: 1.6;
            font-weight: 400;
            color: var(--text-secondary);
            max-width: 30rem;
            margin-bottom: 2.75rem;
            text-wrap: pretty;
        }

        .card-title {
            font-size: 0.74rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }

        /* ----- Generic card ----- */
        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 1px 2px rgba(24, 24, 27, 0.03);
            transition: box-shadow 0.3s ease, border-color 0.3s ease;
        }
        .card:hover {
            border-color: #DAD9D4;
            box-shadow: 0 12px 32px rgba(24, 24, 27, 0.06);
        }

        /* ----- Answer text ----- */
        .answer-text {
            font-size: 1.08rem;
            line-height: 1.75;
            color: var(--text-primary);
        }

        /* ---------- Source Cards ---------- */
        .pill-row{
        display:flex;
        flex-direction:column;
        gap:16px;
        }

        .pill{

        display:flex;
        justify-content:space-between;
        align-items:center;

        background:white;

        border:1px solid #E5E7EB;

        border-radius:18px;

        padding:18px 22px;

        transition:.2s;
    }

    .pill:hover{

        border-color:#2563EB;

        box-shadow:0 10px 20px rgba(0,0,0,.05);

    }

    .pill-file{

        font-size:18px;

        font-weight:600;

        color:#111827;

    }

    .pill-meta{

        font-size:14px;

        color:#6B7280;

        margin-top:4px;

    }

    .pill-conf{

        background:#EEF4FF;

        color:#2563EB;

        padding:8px 14px;

        border-radius:999px;

        font-weight:700;

        font-size:14px;

        white-space:nowrap;
    }

        /* ----- Statistic cards ----- */
        .stat-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem 1.35rem;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        .stat-card:hover {
            border-color: #DAD9D4;
            box-shadow: 0 8px 20px rgba(24, 24, 27, 0.05);
        }
        .stat-label {
            font-size: 0.72rem;
            font-weight: 500;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: 0.45rem;
        }
        .stat-value {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.01em;
        }

        /* ----- Chunk preview ----- */
        .chunk-preview {
            font-size: 0.94rem;
            line-height: 1.65;
            color: var(--text-primary);
            background: #FAFAF9;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin: 0.6rem 0;
        }
        .chunk-meta {
            font-size: 0.82rem;
            color: var(--text-secondary);
        }
        .chunk-score {
            color: var(--accent);
            font-weight: 600;
        }

        /* ----- Text input ----- */
        .stTextInput > div > div > input {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            background: var(--card) !important;
            color: var(--text-primary) !important;
            padding: 1.1rem 1.2rem !important;
            font-size: 1.05rem !important;
            box-shadow: 0 1px 2px rgba(24, 24, 27, 0.03) !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        .stTextInput > div > div > input::placeholder {
            color: #A1A1AA !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1) !important;
        }

        /* ----- Primary button ----- */
        .stButton > button {
            background: var(--text-primary);
            color: #FFFFFF;
            border: none;
            border-radius: 14px;
            padding: 0.9rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            width: 100%;
            transition: background 0.2s ease, transform 0.15s ease,
                        box-shadow 0.2s ease;
        }
        .stButton > button:hover {
            background: var(--accent);
            transform: translateY(-1px);
            box-shadow: 0 10px 24px rgba(37, 99, 235, 0.22);
        }
        .stButton > button:active {
            transform: translateY(0);
        }

        /* ----- Expander (collapsible chunk cards) ----- */
        div[data-testid="stExpander"] summary {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            background: var(--card) !important;
            font-weight: 600 !important;
            color: var(--text-primary) !important;
        }
        div[data-testid="stExpander"] {
            border: none !important;
            margin-bottom: 0.75rem;
        }

        /* ----- Divider label ----- */
        .section-label {
            font-family: 'Fraunces', Georgia, serif;
            font-size: 1.35rem;
            font-weight: 500;
            color: var(--text-primary);
            letter-spacing: -0.01em;
            margin: 2.25rem 0 1rem 0;
        }

        /* ----- Footer ----- */
        .footer {
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.82rem;
            margin-top: 3.5rem;
            padding-top: 1.75rem;
            border-top: 1px solid var(--border);
        }

        /* Hide Streamlit chrome */
        #MainMenu, header, footer {visibility: hidden;}

        /* Eliminate the sidebar and every control that can reopen it */
        section[data-testid="stSidebar"],
        div[data-testid="stSidebar"],
        div[data-testid="stSidebarNav"],
        div[data-testid="stSidebarCollapsedControl"],
        button[data-testid="stSidebarCollapseButton"],
        button[data-testid="baseButton-headerNoPadding"],
        button[kind="header"],
        [data-testid="collapsedControl"] {
            display: none !important;
            width: 0 !important;
            visibility: hidden !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# FastAPI Backend Integration
# ---------------------------------------------------------------------------

import requests

BACKEND_URL = "https://multidoc-rag-hahfdxgtbnhve9ba.centralindia-01.azurewebsites.net"


def ask_backend(question: str):
    """
    Sends the user's question to the FastAPI backend
    and returns the complete JSON response.
    """

    try:

        response = requests.post(
            f"{BACKEND_URL}/query",
            json={"question": question},
            timeout=300,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the backend.\n\n"
            "Make sure FastAPI is running:\n\n"
            "uvicorn main:app --reload"
        )

        return None

    except requests.exceptions.Timeout:

        st.error("The backend took too long to respond.")

        return None

    except requests.exceptions.RequestException as e:

        st.error(str(e))

        return None


# ---------------------------------------------------------------------------
# Rendering helpers
# ---------------------------------------------------------------------------
# def render_answer(answer: str) -> None:
#     st.markdown(
#         f"""
#         <div class="card">
#             <div class="card-title">Answer</div>
#             <div class="answer-text">{answer}</div>
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )
def render_answer(answer):
    st.success(answer)


def display_sources(sources):

    html = """
<div class="card">
<div class="card-title">
Source Documents
</div>

<div class="pill-row">
"""

    for s in sources:

        html += f"""
<div class="pill">

<div>

<div class="pill-file">
📄 {s["file_name"]}
</div>

<div class="pill-meta">
{s["category"]} • Page {s["page"]}
</div>

</div>

<div class="pill-conf">
{s["score"]:.3f}
</div>

</div>
"""

    html += """
</div>
</div>
"""

    st.markdown(dedent(html), unsafe_allow_html=True)


def render_chunks(results) -> None:
    st.markdown(
        '<div class="section-label">Retrieved Chunks</div>', unsafe_allow_html=True
    )
    for r in results:
        with st.expander(
            f"Rank {r['rank']}  ·  {r['file_name']}  ·  score {r['score']}"
        ):
            meta = "  ·  ".join(f"{k}: {v}" for k, v in r["metadata"].items())
            st.markdown(
                f"""
                <div class="chunk-meta">
                    <span class="chunk-score">Retrieval score: {r['score']}</span>
                    &nbsp;·&nbsp; page {r['page']}
                </div>
                <div class="chunk-preview">{r['preview']}</div>
                <div class="chunk-meta">{meta}</div>
                """,
                unsafe_allow_html=True,
            )


def render_stats(latency, retrieved_count, embedding_model, method):

    st.markdown(
        '<div class="section-label">System Statistics</div>',
        unsafe_allow_html=True,
    )

    stats = [
        ("Query Latency", f"{latency:.2f}s"),
        ("Retrieved Chunks", str(retrieved_count)),
        ("Embedding Model", embedding_model.split("/")[-1]),
        ("Retrieval Strategy", method),
        ("Generator", "Groq Llama-3.1"),
        ("Reranker", "Cross Encoder"),
    ]

    for i in range(0, len(stats), 3):

        cols = st.columns(3)

        for col, (label, value) in zip(cols, stats[i : i + 3]):

            with col:

                st.markdown(
                    f"""
                    <div class="stat-card">
                        <div class="stat-label">{label}</div>
                        <div class="stat-value">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def render_ragas():

    st.markdown(
        '<div class="section-label">Offline RAGAS Evaluation</div>',
        unsafe_allow_html=True,
    )

    metrics = [
        ("Faithfulness", 0.7116),
        ("Answer Relevancy", 0.7809),
        ("Context Precision", 0.7532),
        ("Context Recall", 0.8765),
    ]

    cols = st.columns(4)

    for col, (label, score) in zip(cols, metrics):

        if score >= 0.85:
            icon = ""
        elif score >= 0.70:
            icon = ""
        else:
            icon = ""

        with col:

            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value">{icon} {score:.3f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.caption("Offline evaluation using RAGAS with Ollama on the benchmark dataset.")


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------
def main():
    inject_css()

    if "history" not in st.session_state:
        st.session_state.history = []

    # Hero
    st.markdown(
        '<span class="eyebrow">Document Intelligence</span>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-title">Ask your documents<br>' "<em>anything.</em></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Retrieval-augmented generation across your '
        "entire knowledge base — grounded answers with traceable citations.</div>",
        unsafe_allow_html=True,
    )

    # Search area
    query = st.text_input(
        "Question",
        placeholder="What would you like to know?",
        label_visibility="collapsed",
    )
    generate = st.button("Generate Answer")

    # Handle generation
    if generate and query.strip():

        with st.spinner("Retrieving context and generating answer..."):

            response = ask_backend(query)
            st.write("Backend Response:")
            st.json(response)

            if response is None:
                st.stop()

            answer = response["answer"]
            latency = response["latency"]

            # ----------------------------
            # Convert backend sources into
            # the format expected by UI
            # ----------------------------

            results = []

            for source in response["sources"]:

                results.append(
                    {
                        "rank": source["rank"],
                        "score": source["score"],
                        "file_name": source["file_name"],
                        "page": source["page"],
                        "preview": source["preview"],
                        "metadata": {
                            "category": source["category"],
                            "chunk_id": source["chunk_id"],
                        },
                    }
                )

            sources = []

            for source in response["sources"]:

                sources.append(
                    {
                        "file_name": source["file_name"],
                        "page": source["page"] if source["page"] is not None else "-",
                        "category": source["category"],
                        "score": source["score"],
                    }
                )

        st.session_state.history.append(
            {
                "query": query,
                "answer": answer,
                "results": results,
                "sources": sources,
                "latency": latency,
                "timestamp": datetime.now().strftime("%H:%M"),
            }
        )
    # Render most recent result
    if st.session_state.history:
        latest = st.session_state.history[-1]

        st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

        #render_answer(latest["answer"])
        st.write(latest)
        st.success(latest["answer"])
        display_sources(latest["sources"])
        render_chunks(latest["results"])
        render_stats(
            latency=latest["latency"],
            retrieved_count=len(latest["results"]),
            embedding_model=CONFIG["embedding_model"],
            method=CONFIG["method"],
        )
        render_ragas()

    # Footer
    st.markdown(
        '<div class="footer">Built with Streamlit · LangChain · ChromaDB · '
        "HuggingFace Embeddings</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
