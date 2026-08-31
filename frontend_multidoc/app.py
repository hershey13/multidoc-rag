"""
Multi-Document Question Answering
Retrieval-Augmented Generation for Document Intelligence

Premium Streamlit frontend for a FastAPI RAG backend.
"""

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
# Configuration
# ---------------------------------------------------------------------------

CONFIG = {
    "method": "Hybrid + Cross Encoder",
    "embedding_model": "BAAI/bge-small-en-v1.5",
    "chunk_size": 500,
    "top_k": 5,
}


# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------


def inject_css() -> None:
    st.markdown(
        """
        <style>

        /* =========================================================
           Fonts
        ========================================================= */

        @import url(
            'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
            '&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600'
            '&display=swap'
        );

        html,
        body,
        [class*="css"],
        .stApp {
            font-family: 'Inter',
                -apple-system,
                BlinkMacSystemFont,
                'Segoe UI',
                sans-serif;
        }


        /* =========================================================
           Color tokens
        ========================================================= */

        :root {
            --bg: #FAFAF9;
            --card: #FFFFFF;
            --text-primary: #18181B;
            --text-secondary: #71717A;
            --accent: #2563EB;
            --accent-soft: rgba(37, 99, 235, 0.08);
            --border: #EAEAE7;
        }


        /* =========================================================
           App background
        ========================================================= */

        .stApp {
            background:
                radial-gradient(
                    1200px 500px at 50% -10%,
                    rgba(37, 99, 235, 0.05),
                    transparent 70%
                ),
                var(--bg);
        }

        .block-container {
            padding-top: 4.5rem;
            padding-bottom: 5rem;
            max-width: 760px;
        }


        /* =========================================================
           Hero
        ========================================================= */

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


        /* =========================================================
           Generic cards
        ========================================================= */

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 1px 2px rgba(24, 24, 27, 0.03);
            transition:
                box-shadow 0.3s ease,
                border-color 0.3s ease;
        }

        .card:hover {
            border-color: #DAD9D4;
            box-shadow:
                0 12px 32px rgba(24, 24, 27, 0.06);
        }

        .card-title {
            font-size: 0.74rem;
            font-weight: 600;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }


        /* =========================================================
           Answer
        ========================================================= */

        .answer-card {
            background: #FFFFFF;
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1.5rem;
            margin-top: 1.5rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 1px 2px rgba(24, 24, 27, 0.03);
        }

        .answer-header {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--accent);
            margin-bottom: 1rem;
        }

        .answer-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 28px;
            height: 28px;
            border-radius: 9px;
            background: var(--accent-soft);
            font-size: 0.9rem;
        }

        .answer-body {
            font-size: 1.08rem;
            line-height: 1.75;
            color: var(--text-primary);
        }

        .answer-body p {
            margin-top: 0;
            margin-bottom: 1rem;
        }

        .answer-body p:last-child {
            margin-bottom: 0;
        }


        /* =========================================================
           Source cards
        ========================================================= */

        .pill-row {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .pill {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 1rem;

            background: #FFFFFF;

            border: 1px solid #E5E7EB;

            border-radius: 16px;

            padding: 16px 18px;

            transition:
                border-color 0.2s ease,
                box-shadow 0.2s ease,
                transform 0.2s ease;
        }

        .pill:hover {
            border-color: #2563EB;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
            transform: translateY(-1px);
        }

        .pill-file {
            font-size: 0.98rem;
            font-weight: 600;
            color: #111827;
        }

        .pill-meta {
            font-size: 0.82rem;
            color: #6B7280;
            margin-top: 4px;
        }

        .pill-conf {
            background: #EEF4FF;
            color: #2563EB;
            padding: 7px 11px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.78rem;
            white-space: nowrap;
        }


        /* =========================================================
           Statistics
        ========================================================= */

        .stat-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem 1.35rem;
            transition:
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }

        .stat-card:hover {
            border-color: #DAD9D4;
            box-shadow:
                0 8px 20px rgba(24, 24, 27, 0.05);
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
            font-size: 1.2rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.01em;
        }


        /* =========================================================
           Retrieved chunks
        ========================================================= */

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


        /* =========================================================
           Text input
        ========================================================= */

        .stTextInput > div > div > input {
            border-radius: 14px !important;
            border: 1px solid var(--border) !important;
            background: var(--card) !important;
            color: var(--text-primary) !important;
            padding: 1.1rem 1.2rem !important;
            font-size: 1.05rem !important;
            box-shadow:
                0 1px 2px rgba(24, 24, 27, 0.03) !important;

            transition:
                border-color 0.2s ease,
                box-shadow 0.2s ease !important;
        }

        .stTextInput > div > div > input::placeholder {
            color: #A1A1AA !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: var(--accent) !important;
            box-shadow:
                0 0 0 4px rgba(37, 99, 235, 0.1) !important;
        }


        /* =========================================================
           Primary button
        ========================================================= */

        .stButton > button {
            background: var(--text-primary);
            color: #FFFFFF;
            border: none;
            border-radius: 14px;
            padding: 0.9rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            width: 100%;

            transition:
                background 0.2s ease,
                transform 0.15s ease,
                box-shadow 0.2s ease;
        }

        .stButton > button:hover {
            background: var(--accent);
            transform: translateY(-1px);
            box-shadow:
                0 10px 24px rgba(37, 99, 235, 0.22);
        }

        .stButton > button:active {
            transform: translateY(0);
        }


        /* =========================================================
           Expanders
        ========================================================= */

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


        /* =========================================================
           Section labels
        ========================================================= */

        .section-label {
            font-family: 'Fraunces', Georgia, serif;
            font-size: 1.35rem;
            font-weight: 500;
            color: var(--text-primary);
            letter-spacing: -0.01em;
            margin: 2.25rem 0 1rem 0;
        }


        /* =========================================================
           Footer
        ========================================================= */

        .footer {
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.82rem;
            margin-top: 3.5rem;
            padding-top: 1.75rem;
            border-top: 1px solid var(--border);
        }


        /* =========================================================
           Hide Streamlit chrome
        ========================================================= */

        #MainMenu,
        header,
        footer {
            visibility: hidden;
        }


        /* Hide sidebar */
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

BACKEND_URL = (
    "https://multidoc-rag-hahfdxgtbnhve9ba." "centralindia-01.azurewebsites.net"
)


def ask_backend(question: str):
    """
    Send the user's question to the FastAPI backend
    and return the JSON response.
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


def render_answer(answer):
    html = f"""<div class="answer-card">
<div class="answer-header">
<span class="answer-icon">✦</span>
<span>Answer</span>
</div>
<div class="answer-body">
{answer}
</div>
</div>"""

    st.markdown(html, unsafe_allow_html=True)


def display_sources(sources):
    parts = [
        '<div class="card">',
        '<div class="card-title">Source Documents</div>',
        '<div class="pill-row">',
    ]

    for i, s in enumerate(sources, start=1):
        parts.append(f"""
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
        Rank {i}
    </div>
</div>
""")

    parts.extend([
        "</div>",
        "</div>",
    ])

    st.markdown(
        "\n".join(parts),
        unsafe_allow_html=True
    )
def render_chunks(results):
    st.markdown(
        '<div class="section-label">Retrieved Chunks</div>',
        unsafe_allow_html=True,
    )

    for r in results:
        with st.expander(
            f"Rank {r['rank']}  ·  {r['file_name']}  ·  score {r['score']}"
        ):
            meta = "  ·  ".join(
                f"{k}: {v}" for k, v in r["metadata"].items()
            )

            html = f'''<div class="chunk-meta">
<span class="chunk-score">Retrieval score: {r["score"]}</span>
&nbsp;·&nbsp; page {r["page"]}
</div>
<div class="chunk-preview">
{r["preview"]}
</div>
<div class="chunk-meta">
{meta}
</div>'''

            st.markdown(html, unsafe_allow_html=True)


def render_stats(
    latency,
    retrieved_count,
    embedding_model,
    method,
):
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

        for col, (label, value) in zip(cols, stats[i:i + 3]):
            html = f'''<div class="stat-card">
<div class="stat-label">{label}</div>
<div class="stat-value">{value}</div>
</div>'''

            with col:
                st.markdown(html, unsafe_allow_html=True)


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

    for row in (metrics[:2], metrics[2:]):
        cols = st.columns(2)

        for col, (label, score) in zip(cols, row):
            html = f'''<div class="stat-card">
<div class="stat-label">{label}</div>
<div class="stat-value">● {score:.3f}</div>
</div>'''

            with col:
                st.markdown(html, unsafe_allow_html=True)

    st.caption(
        "Offline evaluation using RAGAS with Ollama "
        "on the benchmark dataset."
    )


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------


def main():

    inject_css()

    if "history" not in st.session_state:
        st.session_state.history = []

    # =========================================================
    # Hero
    # =========================================================

    st.markdown(
        '<span class="eyebrow">Document Intelligence</span>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-title">'
        "Ask your documents<br>"
        "<em>anything.</em>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">'
        "Get grounded answers from your company documents, "
        "with sources you can verify."
        "</div>",
        unsafe_allow_html=True,
    )

    # =========================================================
    # Search area
    # =========================================================

    query = st.text_input(
        "Question",
        placeholder="What would you like to know?",
        label_visibility="collapsed",
    )

    generate = st.button("Ask MultiDoc AI  →")

    # =========================================================
    # Handle generation
    # =========================================================

    if generate and query.strip():

        with st.spinner("Retrieving context and generating answer..."):

            response = ask_backend(query)

            if response is None:
                st.stop()

            answer = response.get(
                "answer",
                "",
            )

            latency = response.get(
                "latency",
                0,
            )

            # -------------------------------------------------
            # Convert backend sources into UI format
            # -------------------------------------------------

            results = []

            for source in response.get("sources", []):

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

            for source in response.get("sources", []):

                sources.append(
                    {
                        "file_name": source["file_name"],
                        "page": (source["page"] if source["page"] is not None else "-"),
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

    # =========================================================
    # Render latest result
    # =========================================================

    if st.session_state.history:

        latest = st.session_state.history[-1]

        st.markdown(
            "<div style='height:2rem;'></div>",
            unsafe_allow_html=True,
        )

        # Main answer
        render_answer(latest["answer"])

        # Source documents
        display_sources(latest["sources"])

        # Technical information
        with st.expander(
            "Retrieved context",
            expanded=False,
        ):
            render_chunks(latest["results"])

        with st.expander(
            "Technical details",
            expanded=False,
        ):
            render_stats(
                latency=latest["latency"],
                retrieved_count=len(latest["results"]),
                embedding_model=CONFIG["embedding_model"],
                method=CONFIG["method"],
            )

        with st.expander(
            "RAGAS evaluation",
            expanded=False,
        ):
            render_ragas()

    # =========================================================
    # Footer
    # =========================================================

    st.markdown(
        '<div class="footer">'
        "Built with Streamlit · LangChain · ChromaDB · "
        "HuggingFace Embeddings"
        "</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
