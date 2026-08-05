from groq import Groq
from langchain_ollama import ChatOllama

from config import *

groq_client = None
ollama_llm = None


def get_llm():

    global groq_client
    global ollama_llm

    if LLM_PROVIDER == "groq":

        if groq_client is None:

            groq_client = Groq(
                api_key=GROQ_API_KEY,
            )

        return groq_client

    elif LLM_PROVIDER == "ollama":

        if ollama_llm is None:

            ollama_llm = ChatOllama(
                model=OLLAMA_MODEL,
                temperature=TEMPERATURE,
            )

        return ollama_llm

    raise ValueError(f"Unknown provider {LLM_PROVIDER}")


def build_prompt(question, contexts):

    context = "\n\n----------------\n\n".join(contexts)

    return f"""
You are an AI assistant answering questions using retrieved company documents.

Instructions:

- Answer ONLY from the provided context.
- If the answer requires combining information from multiple passages, do so.
- Summarize instead of copying large chunks verbatim.
- If the context partially answers the question, provide the partial answer and mention any missing details.
- Only reply "I couldn't find this information in the provided documents." if NONE of the retrieved passages contain relevant information.

Question:
{question}

Retrieved Context:
{context}

Answer:
"""


def generate(question, retrieval_results):

    contexts = [r.document.page_content for r in retrieval_results]

    prompt = build_prompt(
        question,
        contexts,
    )
    print("=" * 80)
    print(prompt)
    print("=" * 80)
    if LLM_PROVIDER == "groq":

        client = get_llm()

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        answer = response.choices[0].message.content

    else:

        llm = get_llm()

        answer = llm.invoke(prompt).content

    return {
        "answer": answer,
        "contexts": contexts,
    }
