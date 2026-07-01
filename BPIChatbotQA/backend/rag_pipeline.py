"""
rag_pipeline.py — RAG (Retrieval-Augmented Generation) core logic
Supports both Groq (cloud, fast, free) and Ollama (local).
"""

import os
import sys

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

sys.path.insert(0, os.path.dirname(__file__))
from config import (
    VECTORSTORE_PATH, COLLECTION_NAME, EMBEDDING_MODEL,
    OLLAMA_BASE_URL, LLM_MODEL, TOP_K_DOCS,
    USE_GROQ, GROQ_API_KEY, GROQ_MODEL,
)

# ── Prompt Template ────────────────────────────────────────────────────────────
# This tells the LLM exactly how to behave: answer ONLY from the documents,
# say "I don't know" if the answer isn't there — avoids hallucinations
RAG_PROMPT_TEMPLATE = """You are the BPI Q&A assistant helping SIT and UAT testers understand system behavior, user stories, and design documents.

Use the context provided below to answer the question as accurately and completely as possible.
The context contains user stories written in GIVEN/WHEN/THEN format — extract and explain them clearly.
Only say "I could not find this information" if the context is completely empty or totally unrelated.
Do NOT make up information that is not in the context. Be concise, factual, and helpful.

Context from documents:
-----------------------
{context}
-----------------------

Tester's Question: {question}

Answer (based on the context above):"""

RAG_PROMPT = PromptTemplate(
    template=RAG_PROMPT_TEMPLATE,
    input_variables=["context", "question"],
)

# ── Singleton instances (loaded once, reset on re-ingest) ─────────────────────
_embeddings  = None
_vectorstore = None
_qa_chain    = None
_chain_lock  = __import__("threading").Lock()  # thread-safe reset


def _get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings


def _get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        if not os.path.exists(VECTORSTORE_PATH):
            raise FileNotFoundError(
                f"Vector store not found at '{VECTORSTORE_PATH}'. "
                "Run 'python ingest.py' first to load your documents."
            )
        _vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=VECTORSTORE_PATH,
            embedding_function=_get_embeddings(),
        )
    return _vectorstore


def reset_pipeline():
    """
    Fully reset the RAG pipeline after re-ingestion.
    Called by watcher after vectorstore is rebuilt on disk.
    Forces fresh Chroma connection + new retriever + new chain on next question.
    """
    global _vectorstore, _qa_chain
    with _chain_lock:
        # Close existing vectorstore connection if possible
        try:
            if _vectorstore is not None:
                _vectorstore._client.reset()
        except Exception:
            pass
        _vectorstore = None
        _qa_chain    = None
    print("[RAG] Pipeline reset — will reload fresh vectorstore on next question.")


def _build_llm():
    """Return Groq or Ollama LLM based on config."""
    if USE_GROQ:
        from langchain_groq import ChatGroq
        print(f"[RAG] Using Groq API — model: {GROQ_MODEL}")
        return ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
            temperature=0.1,
            max_tokens=768,
        )
    else:
        from langchain_ollama import OllamaLLM
        print(f"[RAG] Using Ollama local — model: {LLM_MODEL}")
        return OllamaLLM(
            model=LLM_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.1,
            num_predict=768,
            num_ctx=4096,
        )


def get_qa_chain():
    global _qa_chain
    with _chain_lock:
        if _qa_chain is None:
            llm = _build_llm()
            retriever = _get_vectorstore().as_retriever(
                search_type="mmr",
                search_kwargs={"k": 6, "fetch_k": 12},
            )
            _qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": RAG_PROMPT},
            )
    return _qa_chain


def ask_question(question: str) -> dict:
    """
    Ask a question and return the answer + source documents.
    Returns: { "answer": str, "sources": [{"file": str, "snippet": str}] }
    """
    chain  = get_qa_chain()
    result = chain.invoke({"query": question})

    answer = result.get("result", "").strip()

    # Collect unique source files and a short snippet from each
    sources = []
    seen_files = set()
    for doc in result.get("source_documents", []):
        fname = doc.metadata.get("source_file", doc.metadata.get("source", "Unknown"))
        if fname not in seen_files:
            seen_files.add(fname)
            snippet = doc.page_content[:200].replace("\n", " ").strip()
            sources.append({"file": fname, "snippet": snippet + "…"})

    return {"answer": answer, "sources": sources}


def is_vectorstore_ready() -> bool:
    """Check whether documents have been ingested."""
    try:
        vs = _get_vectorstore()
        return vs._collection.count() > 0
    except Exception:
        return False


def prewarm():
    """
    Pre-load the model at server startup so the first real question is fast.
    Sends a trivial prompt to Ollama to pull the model into RAM.
    """
    try:
        print(f"  Pre-warming model '{LLM_MODEL}' — please wait...")
        get_qa_chain()
        # Minimal warm-up: initialises embeddings + retriever at startup
        print(f"  Model chain ready.")
    except Exception as e:
        print(f"  [WARN] Pre-warm failed: {e}")
