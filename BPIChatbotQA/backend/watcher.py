"""
watcher.py — Automatic document re-ingestion using watchdog
Monitors DOCS_PATH and re-ingests when files are closed after editing.

Key behaviours:
  - Ignores Word/Excel temp files (~$filename)
  - Waits until file is fully released (closed by Word/PDF viewer)
  - 20-second debounce — collects all changes then ingests once
  - Works for: create, update, delete, rename of .pdf .docx .txt .md
"""

import os
import sys
import time
import threading
import logging

from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

sys.path.insert(0, os.path.dirname(__file__))
from config import DOCS_PATH, VECTORSTORE_PATH, COLLECTION_NAME, EXCLUDED_FILES

logger = logging.getLogger("bpi_watcher")
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s", datefmt="%H:%M:%S")

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}
DEBOUNCE_SECONDS     = 20   # wait 20s after last change — gives Word time to fully close
MAX_LOCK_WAIT        = 60   # max seconds to wait for a locked file to be released
LOCK_POLL_INTERVAL   = 3    # check every 3 seconds if file is still locked

_ingest_timer = None
_ingest_lock  = threading.Lock()

watcher_status = {
    "watching":       False,
    "last_event":     None,
    "last_ingest":    None,
    "ingest_pending": False,
    "error":          None,
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def _is_supported(path: str) -> bool:
    """Return True only for real supported files — skip Word temp files."""
    name = os.path.basename(path)
    ext  = os.path.splitext(name)[1].lower()
    # Skip Word temp files (~$Doc.docx), hidden files, lock files
    if name.startswith("~$") or name.startswith(".") or name.endswith(".tmp"):
        return False
    excluded_lower = [f.lower() for f in EXCLUDED_FILES]
    if name.lower() in excluded_lower:
        return False
    return ext in SUPPORTED_EXTENSIONS


def _is_file_released(path: str) -> bool:
    """
    Check if a file is fully closed and readable.
    Word / PDF viewers hold an exclusive lock while the file is open.
    We try opening in binary read mode — if it succeeds the file is released.
    """
    if not os.path.exists(path):
        return True   # deleted — that's fine, proceed with ingest
    try:
        with open(path, "rb") as f:
            f.read(1)
        return True
    except (PermissionError, OSError):
        return False


def _wait_until_released(path: str) -> bool:
    """
    Poll until the file is released by Word/PDF viewer.
    Returns True when released, False if timed out.
    """
    if not os.path.exists(path):
        return True   # deleted — ok to proceed
    elapsed = 0
    while elapsed < MAX_LOCK_WAIT:
        if _is_file_released(path):
            logger.info("[Watcher] File released — ready to ingest: %s", os.path.basename(path))
            return True
        logger.info("[Watcher] File still open in Word/PDF viewer, waiting... (%ds)", elapsed)
        time.sleep(LOCK_POLL_INTERVAL)
        elapsed += LOCK_POLL_INTERVAL
    logger.warning("[Watcher] File not released after %ds — skipping: %s", MAX_LOCK_WAIT, path)
    return False


# ── Ingest ─────────────────────────────────────────────────────────────────────

def _run_ingest(trigger_file: str):
    """
    Rebuild the entire vector store from all current docs in DOCS_PATH.
    Called in a background thread after debounce.
    """
    import shutil
    from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from config import EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP

    # Wait until the triggering file is fully closed
    if trigger_file and os.path.exists(trigger_file):
        if not _wait_until_released(trigger_file):
            watcher_status["ingest_pending"] = False
            watcher_status["error"] = f"File locked — could not read: {os.path.basename(trigger_file)}"
            return

    logger.info("[Watcher] ====== Starting auto-ingest ======")
    watcher_status["ingest_pending"] = True
    watcher_status["error"]          = None

    try:
        excluded_lower = [f.lower() for f in EXCLUDED_FILES]
        docs = []

        for root, _, files in os.walk(DOCS_PATH):
            for fname in sorted(files):
                ext = os.path.splitext(fname)[1].lower()
                if ext not in SUPPORTED_EXTENSIONS:
                    continue
                if fname.lower() in excluded_lower:
                    logger.info("[Watcher] Skipping excluded: %s", fname)
                    continue
                if fname.startswith("~$") or fname.startswith("."):
                    continue   # skip Word temp/lock files

                fpath = os.path.join(root, fname)

                # Skip if still locked
                if not _is_file_released(fpath):
                    logger.warning("[Watcher] Skipping locked file: %s", fname)
                    continue

                try:
                    if ext == ".pdf":
                        loader = PyPDFLoader(fpath)
                    elif ext == ".docx":
                        loader = Docx2txtLoader(fpath)
                    else:
                        try:
                            loader = TextLoader(fpath, encoding="utf-8")
                            loader.load()
                            loader = TextLoader(fpath, encoding="utf-8")
                        except Exception:
                            loader = TextLoader(fpath, encoding="cp1252")

                    loaded = loader.load()
                    for doc in loaded:
                        doc.metadata["source_file"] = fname
                    docs.extend(loaded)
                    logger.info("[Watcher] ✅ Loaded: %s (%d page(s))", fname, len(loaded))

                except Exception as e:
                    logger.warning("[Watcher] ⚠️  Could not load %s: %s", fname, e)

        if not docs:
            logger.warning("[Watcher] No documents found — vector store unchanged.")
            watcher_status["ingest_pending"] = False
            return

        # Split into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        chunks = splitter.split_documents(docs)
        logger.info("[Watcher] %d chunks from %d pages", len(chunks), len(docs))

        # Clear old vector store
        if os.path.exists(VECTORSTORE_PATH):
            shutil.rmtree(VECTORSTORE_PATH)

        # Rebuild embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            persist_directory=VECTORSTORE_PATH,
        )

        # Fully reset RAG pipeline so next question loads fresh vectorstore from disk
        import rag_pipeline
        rag_pipeline.reset_pipeline()

        watcher_status["last_ingest"]    = time.strftime("%Y-%m-%d %H:%M:%S")
        watcher_status["ingest_pending"] = False
        watcher_status["error"]          = None
        logger.info("[Watcher] ====== Auto-ingest complete — %d vectors ======", len(chunks))

    except Exception as e:
        logger.error("[Watcher] Ingest failed: %s", e)
        watcher_status["error"]          = str(e)
        watcher_status["ingest_pending"] = False


def _schedule_ingest(trigger_file: str):
    """
    Debounce: reset the countdown on every new file event.
    Only fires _run_ingest once all changes have settled (20s of quiet).
    """
    global _ingest_timer
    with _ingest_lock:
        if _ingest_timer and _ingest_timer.is_alive():
            _ingest_timer.cancel()

        watcher_status["last_event"]     = os.path.basename(trigger_file)
        watcher_status["ingest_pending"] = True
        logger.info("[Watcher] Change: %s — re-ingest in %ds",
                    os.path.basename(trigger_file), DEBOUNCE_SECONDS)

        _ingest_timer = threading.Timer(
            DEBOUNCE_SECONDS,
            lambda: threading.Thread(
                target=_run_ingest,
                args=(trigger_file,),
                daemon=True
            ).start()
        )
        _ingest_timer.daemon = True
        _ingest_timer.start()


# ── Event Handler ──────────────────────────────────────────────────────────────

class DocsEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory and _is_supported(event.src_path):
            logger.info("[Watcher] NEW: %s", os.path.basename(event.src_path))
            _schedule_ingest(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and _is_supported(event.src_path):
            logger.info("[Watcher] MODIFIED: %s", os.path.basename(event.src_path))
            _schedule_ingest(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory and _is_supported(event.src_path):
            logger.info("[Watcher] DELETED: %s", os.path.basename(event.src_path))
            _schedule_ingest(event.src_path)

    def on_moved(self, event):
        if not event.is_directory and _is_supported(event.dest_path):
            logger.info("[Watcher] RENAMED to: %s", os.path.basename(event.dest_path))
            _schedule_ingest(event.dest_path)


# ── Start ──────────────────────────────────────────────────────────────────────

def start_watcher():
    """
    Start the background file watcher.
    Uses PollingObserver for network shares (\\server\share), native Observer for local.
    """
    if not os.path.exists(DOCS_PATH):
        logger.warning("[Watcher] Path not found — watcher not started: %s", DOCS_PATH)
        watcher_status["watching"] = False
        return

    handler  = DocsEventHandler()
    is_share = DOCS_PATH.startswith("\\\\") or DOCS_PATH.startswith("//")
    observer = PollingObserver(timeout=15) if is_share else Observer()

    observer.schedule(handler, path=DOCS_PATH, recursive=True)
    observer.daemon = True
    observer.start()

    watcher_status["watching"] = True
    mode = "PollingObserver (network)" if is_share else "Observer (local)"
    logger.info("[Watcher] Started — watching: %s  [%s]", DOCS_PATH, mode)
    logger.info("[Watcher] Triggers: .pdf .docx .txt .md  |  Debounce: %ds  |  Lock-wait: %ds",
                DEBOUNCE_SECONDS, MAX_LOCK_WAIT)
