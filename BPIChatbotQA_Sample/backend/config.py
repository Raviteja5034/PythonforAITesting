"""
config.py — Central configuration for BPI-IBM QA Chatbot
"""

import os

# ─── Document Source ──────────────────────────────────────────────────────────
DOCS_PATH = os.environ.get("BPI_DOCS_PATH", r"C:\Users\RavitejaPalakurthi\Documents\Archive")

# ─── Excluded Files ───────────────────────────────────────────────────────────
EXCLUDED_FILES = [
    "sample_rag_test.pdf",
]

# ─── Vector Store ─────────────────────────────────────────────────────────────
VECTORSTORE_PATH = "vectorstore"
COLLECTION_NAME  = "bpi_qa_docs"
MANIFEST_PATH    = os.path.join(VECTORSTORE_PATH, "ingest_manifest.json")

# ─── Embedding Model (local, FREE) ────────────────────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ─── LLM Provider ─────────────────────────────────────────────────────────────
# Set USE_GROQ = True  → uses Groq cloud API (fast, free, no GPU needed)
# Set USE_GROQ = False → uses Ollama local model (slow on CPU, no internet needed)
USE_GROQ = True

# ─── Groq Settings (used when USE_GROQ = True) ────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL   = "llama-3.3-70b-versatile"   # latest Groq free model (replaces llama3-70b-8192)

# ─── Ollama Settings (used when USE_GROQ = False) ─────────────────────────────
OLLAMA_BASE_URL = "http://localhost:11434"
LLM_MODEL       = "llama3.2"

# ─── RAG Settings ─────────────────────────────────────────────────────────────
CHUNK_SIZE    = 800
CHUNK_OVERLAP = 100
TOP_K_DOCS    = 5
