"""
ingest.py — Document ingestion pipeline
Run this script once (or whenever you add new docs) to:
  1. Load all PDF / DOCX / TXT files from DOCS_PATH
  2. Split them into chunks
  3. Embed with HuggingFace (all-MiniLM-L6-v2)
  4. Store in ChromaDB (local vector database)

Usage:
    python ingest.py
    python ingest.py --path "\\\\SERVER\\Share\\TestDocs"
"""

import os
import sys
import argparse
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    DirectoryLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ── allow running from repo root or backend/ ──────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))
sys.path.insert(0, os.path.dirname(__file__))
from config import (
    DOCS_PATH, VECTORSTORE_PATH, COLLECTION_NAME,
    EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, EXCLUDED_FILES,
)

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


def load_documents(docs_path: str):
    """Load all supported documents from a directory (including sub-folders)."""
    path = Path(docs_path)
    if not path.exists():
        print(f"[ERROR] Path does not exist: {docs_path}")
        sys.exit(1)

    docs = []
    files_found = 0

    excluded_lower = [f.lower() for f in EXCLUDED_FILES]

    for file_path in path.rglob("*"):
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        if file_path.name.lower() in excluded_lower:
            print(f"  [SKIP] Excluded: {file_path.name}")
            continue
        files_found += 1
        try:
            ext = file_path.suffix.lower()
            if ext == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif ext == ".docx":
                loader = Docx2txtLoader(str(file_path))
            else:  # .txt or .md
                # Try UTF-8 first, fall back to Windows-1252 (common on corporate PCs)
                try:
                    loader = TextLoader(str(file_path), encoding="utf-8")
                    loader.load()   # test-load to catch encoding errors early
                    loader = TextLoader(str(file_path), encoding="utf-8")
                except Exception:
                    loader = TextLoader(str(file_path), encoding="cp1252")

            loaded = loader.load()
            # Tag each chunk with its source file name
            for doc in loaded:
                doc.metadata["source_file"] = file_path.name
            docs.extend(loaded)
            print(f"  [OK] Loaded: {file_path.name}  ({len(loaded)} page(s)/section(s))")
        except Exception as e:
            print(f"  [WARN] Could not load {file_path.name}: {e}")

    print(f"\nTotal files found   : {files_found}")
    print(f"Total document pages: {len(docs)}")
    return docs


def split_documents(docs):
    """Split documents into overlapping chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"Total chunks created: {len(chunks)}")
    return chunks


def build_vectorstore(chunks, docs_path: str):
    """Embed chunks and persist to ChromaDB."""
    print(f"\nLoading embedding model: {EMBEDDING_MODEL}")
    print("(First run downloads ~80 MB — subsequent runs use cache)")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    print(f"Building vector store at: {VECTORSTORE_PATH}")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=VECTORSTORE_PATH,
    )
    print(f"Vector store ready — {vectordb._collection.count()} vectors stored.\n")
    return vectordb


def main():
    parser = argparse.ArgumentParser(description="BPI Q&A — Document Ingestion")
    parser.add_argument(
        "--path", default=DOCS_PATH,
        help="Path to documents folder or network share"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  BPI Q&A — Document Ingestion Pipeline")
    print("=" * 60)
    print(f"Source path: {args.path}\n")

    docs   = load_documents(args.path)
    if not docs:
        print("[ERROR] No documents found. Add .pdf / .docx / .txt files and retry.")
        sys.exit(1)

    chunks = split_documents(docs)
    build_vectorstore(chunks, args.path)

    print("Ingestion complete! You can now start the backend server.")
    print("  python backend/main.py")


if __name__ == "__main__":
    main()
