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
from config import DOCS_PATH, EXCLUDED_FILES, MANIFEST_PATH
from sync_coordinator import run_synchronized_sync, get_sync_state

logger = logging.getLogger("bpi_watcher")
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(message)s", datefmt="%H:%M:%S")

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".xlsx", ".txt", ".md"}
DEBOUNCE_SECONDS      = 2   # faster debounce for near-real-time sync
MAX_LOCK_WAIT         = 15  # shorter wait to avoid long blocked syncs
LOCK_POLL_INTERVAL    = 1   # check every second if file is still locked
PERIODIC_SYNC_SECONDS = 5   # periodic reconciliation so manual ingest is not needed

_ingest_timer = None
_ingest_lock  = threading.Lock()
_last_scheduled_file = None
_last_schedule_time = 0.0
EVENT_COOLDOWN_SECONDS = 8
MAX_PENDING_SECONDS = 90

watcher_status = {
    "watching": False,
    "last_event": None,
    "last_ingest": None,
    "ingest_pending": False,
    "sync_state": "idle",
    "error": None,
    "last_sync_summary": None,
    "manifest_path": MANIFEST_PATH,
    "periodic_sync_active": False,
    "last_periodic_sync": None,
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

def _set_sync_state(state: str, pending: bool | None = None, error: str | None = None):
    watcher_status["sync_state"] = state
    if pending is not None:
        watcher_status["ingest_pending"] = pending
    if error is not None:
        watcher_status["error"] = error


def _clear_stuck_pending():
    """Clear stale pending state if repeated events prevented sync from starting."""
    with _ingest_lock:
        if watcher_status.get("sync_state") in {"scheduled", "running"} and not watcher_status.get("last_ingest"):
            _set_sync_state("failed", pending=False, error="Watcher pending state timed out before sync could start.")
            logger.warning("[Watcher] Pending state timed out before sync start.")


def _run_ingest(trigger_file: str):
    """Run the same ingest.py flow automatically so watcher behavior matches manual ingest."""
    import subprocess

    if trigger_file and os.path.exists(trigger_file):
        if not _wait_until_released(trigger_file):
            watcher_status["ingest_pending"] = False
            watcher_status["error"] = f"File locked — could not read: {os.path.basename(trigger_file)}"
            return

    logger.info("[Watcher] ====== Starting auto-sync ======")
    _set_sync_state("running", pending=True, error=None)

    def _invoke_ingest():
        ingest_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ingest.py")
        return subprocess.run(
            [sys.executable, ingest_script, "--path", DOCS_PATH],
            capture_output=True,
            text=True,
            timeout=300,
        )

    try:
        sync_run = run_synchronized_sync(_invoke_ingest, reason=f"watcher:{os.path.basename(trigger_file) if trigger_file else 'unknown'}")
        if sync_run["status"] == "busy":
            _set_sync_state("running", pending=True)
            logger.info("[Watcher] Sync already running — keeping pending state for %s", trigger_file)
            return

        result = sync_run["result"]
        if result.returncode != 0:
            raise RuntimeError(result.stderr or result.stdout or "auto-ingest failed")

        import rag_pipeline
        rag_pipeline.reset_pipeline()

        watcher_status["last_ingest"] = time.strftime("%Y-%m-%d %H:%M:%S")
        _set_sync_state("completed", pending=False, error=None)
        watcher_status["last_sync_summary"] = {
            "stdout": result.stdout[-2000:] if result.stdout else "",
            "stderr": result.stderr[-1000:] if result.stderr else "",
            "returncode": result.returncode,
        }
        logger.info("[Watcher] ====== Auto-sync complete ======")
    except Exception as e:
        logger.error("[Watcher] Sync failed: %s", e)
        _set_sync_state("failed", pending=False, error=str(e))


def _schedule_ingest(trigger_file: str):
    """
    Debounce: reset the countdown on every new file event.
    Only fires _run_ingest once all changes have settled (20s of quiet).
    Also suppresses duplicate rapid-fire events for the same file.
    """
    global _ingest_timer, _last_scheduled_file, _last_schedule_time
    with _ingest_lock:
        now = time.time()
        base_name = os.path.basename(trigger_file)

        if (
            watcher_status.get("ingest_pending")
            and _last_scheduled_file == trigger_file
            and (now - _last_schedule_time) < EVENT_COOLDOWN_SECONDS
        ):
            watcher_status["last_event"] = base_name
            logger.info("[Watcher] Duplicate event suppressed for %s", base_name)
            return

        if _ingest_timer and _ingest_timer.is_alive():
            _ingest_timer.cancel()

        _last_scheduled_file = trigger_file
        _last_schedule_time = now
        watcher_status["last_event"] = base_name
        _set_sync_state("scheduled", pending=True)
        logger.info("[Watcher] Change: %s — re-ingest in %ds", base_name, DEBOUNCE_SECONDS)

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

        timeout_timer = threading.Timer(MAX_PENDING_SECONDS, _clear_stuck_pending)
        timeout_timer.daemon = True
        timeout_timer.start()


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


def _periodic_sync_loop():
    """Periodic reconciliation loop so the app stays in sync without manual ingest.py runs."""
    while True:
        try:
            time.sleep(PERIODIC_SYNC_SECONDS)
            watcher_status["periodic_sync_active"] = True
            current_state = watcher_status.get("sync_state", "idle")
            if current_state in {"scheduled", "running"}:
                watcher_status["last_periodic_sync"] = time.strftime("%Y-%m-%d %H:%M:%S")
                continue
            _run_ingest("periodic-sync")
            watcher_status["last_periodic_sync"] = time.strftime("%Y-%m-%d %H:%M:%S")
            if watcher_status.get("sync_state") == "completed" and watcher_status.get("last_event") in {None, "periodic-sync"}:
                _set_sync_state("idle", pending=False)
        except Exception as exc:
            watcher_status["error"] = f"Periodic sync failed: {exc}"
            logger.error("[Watcher] Periodic sync failed: %s", exc)
        finally:
            watcher_status["periodic_sync_active"] = False


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
    logger.info("[Watcher] Triggers: .pdf .docx .pptx .xlsx .txt .md  |  Debounce: %ds  |  Lock-wait: %ds",
                DEBOUNCE_SECONDS, MAX_LOCK_WAIT)

    # Immediate startup sync so manual ingest.py is not required.
    threading.Thread(target=_run_ingest, args=("startup-sync",), daemon=True).start()
    # Periodic reconciliation as a safety net for missed or noisy file events.
    threading.Thread(target=_periodic_sync_loop, daemon=True).start()
