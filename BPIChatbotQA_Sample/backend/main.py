"""
main.py — FastAPI backend server for BPI Q&A Chatbot
Exposes:
  GET  /          → serves the frontend HTML
  GET  /health    → health check (Ollama + vectorstore status)
  POST /ask       → takes a question, returns answer + sources
  POST /ingest    → triggers re-ingestion from configured docs path
"""

import os
import sys
import subprocess
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(__file__))
from rag_pipeline import ask_question, is_vectorstore_ready, prewarm, reset_pipeline, get_vectorstore_count
from watcher import start_watcher, watcher_status
from config import DOCS_PATH, LLM_MODEL, OLLAMA_BASE_URL, USE_GROQ, GROQ_MODEL
from sync_coordinator import run_synchronized_sync, get_sync_state

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="BPI-IBM QA Chatbot",
    description="BPI-IBM QA Chatbot — RAG-powered assistant for SIT/UAT testers",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files at root so relative paths (style.css, app.js) work
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")


# ── Request/Response Models ────────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list
    model: str


class HealthResponse(BaseModel):
    status: str
    vectorstore_ready: bool
    ollama_model: str
    docs_path: str
    message: str
    watcher_active: bool
    last_ingest: str | None
    ingest_pending: bool
    last_changed_file: str | None


class StatusResponse(BaseModel):
    docs_path: str
    vectorstore_ready: bool
    collection_count: int
    watcher_active: bool
    ingest_pending: bool
    last_ingest: str | None
    last_changed_file: str | None
    error: str | None
    manifest_path: str | None
    last_sync_summary: dict | None
    sync_state: dict


# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/", response_class=FileResponse)
def serve_ui():
    """Serve the chatbot UI."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "BPI Q&A API is running. Frontend not found — open frontend/index.html directly."}


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Check if the system is ready to answer questions."""
    vs_ready = is_vectorstore_ready()
    pending    = watcher_status.get("ingest_pending", False)
    active_llm = f"Groq/{GROQ_MODEL}" if USE_GROQ else f"Ollama/{LLM_MODEL}"
    return HealthResponse(
        status="ingesting" if pending else ("ready" if vs_ready else "not_ready"),
        vectorstore_ready=vs_ready,
        ollama_model=active_llm,
        docs_path=DOCS_PATH,
        message=(
            "Re-ingesting new documents — answers updating shortly…"
            if pending
            else ("System ready. Ask your questions!" if vs_ready
                  else "No documents loaded. Run 'python ingest.py' first.")
        ),
        watcher_active=watcher_status.get("watching", False),
        last_ingest=watcher_status.get("last_ingest"),
        ingest_pending=pending,
        last_changed_file=watcher_status.get("last_event"),
    )


@app.post("/ask", response_model=AnswerResponse)
def ask(request: QuestionRequest):
    """Answer a tester's question using RAG."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        from ingest import synchronize_documents
        sync_run = run_synchronized_sync(lambda: synchronize_documents(DOCS_PATH), reason="ask")
        if sync_run["status"] == "ok":
            stats = sync_run["result"]
            if stats.loaded_files or stats.deleted_files or stats.failed_files or stats.skipped_files:
                reset_pipeline()
    except Exception:
        # Do not block answering if background sync check fails.
        pass

    if not is_vectorstore_ready():
        raise HTTPException(
            status_code=503,
            detail="Documents not yet loaded. Please run 'python ingest.py' first, then restart the server.",
        )

    try:
        result = ask_question(request.question)
        return AnswerResponse(
            answer=result["answer"],
            sources=result["sources"],
            model=GROQ_MODEL if USE_GROQ else LLM_MODEL,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")


@app.post("/ingest")
def trigger_ingest():
    """Re-run document ingestion (useful after adding new docs)."""
    try:
        ingest_script = Path(__file__).parent.parent / "ingest.py"
        result = subprocess.run(
            [sys.executable, str(ingest_script)],
            capture_output=True, text=True, timeout=300,
        )
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)
        return {"status": "success", "message": "Documents re-ingested successfully.", "output": result.stdout}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Ingestion timed out (too many documents?).")


@app.get("/status", response_model=StatusResponse)
def status_check():
    return StatusResponse(
        docs_path=DOCS_PATH,
        vectorstore_ready=is_vectorstore_ready(),
        collection_count=get_vectorstore_count(),
        watcher_active=watcher_status.get("watching", False),
        ingest_pending=watcher_status.get("ingest_pending", False),
        last_ingest=watcher_status.get("last_ingest"),
        last_changed_file=watcher_status.get("last_event"),
        error=watcher_status.get("error"),
        manifest_path=watcher_status.get("manifest_path"),
        last_sync_summary=watcher_status.get("last_sync_summary"),
        sync_state=get_sync_state(),
    )


# ── Run directly ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 55)
    print("  BPI-IBM QA Chatbot — Backend Server")
    print("=" * 55)
    active = f"Groq ({GROQ_MODEL})" if USE_GROQ else f"Ollama ({LLM_MODEL})"
    print(f"  Model     : {active}")
    print(f"  Docs path : {DOCS_PATH}")
    print(f"  UI        : http://localhost:8000")
    print(f"  API docs  : http://localhost:8000/docs")
    print("=" * 55 + "\n")
    # Pre-warm embeddings + retriever chain before accepting requests
    if is_vectorstore_ready():
        prewarm()
    # Start file watcher only on local — not needed on cloud (Render)
    is_cloud = os.environ.get("RENDER") == "true"
    if not is_cloud:
        start_watcher()
    else:
        print("  Cloud mode — file watcher disabled (use /ingest API to update docs)")
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
