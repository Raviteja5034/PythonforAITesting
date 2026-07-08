import threading
import time


_sync_lock = threading.Lock()
_sync_state = {
    "running": False,
    "last_started": None,
    "last_finished": None,
    "last_reason": None,
    "last_result": None,
    "last_error": None,
}


def get_sync_state() -> dict:
    with _sync_lock:
        return dict(_sync_state)


def run_synchronized_sync(sync_callable, reason: str):
    with _sync_lock:
        if _sync_state["running"]:
            return {"status": "busy", "state": dict(_sync_state), "result": None}
        _sync_state["running"] = True
        _sync_state["last_started"] = time.strftime("%Y-%m-%d %H:%M:%S")
        _sync_state["last_reason"] = reason
        _sync_state["last_error"] = None

    try:
        result = sync_callable()
        with _sync_lock:
            _sync_state["running"] = False
            _sync_state["last_finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
            _sync_state["last_result"] = {
                "loaded_files": getattr(result, "loaded_files", 0),
                "deleted_files": getattr(result, "deleted_files", 0),
                "failed_files": getattr(result, "failed_files", 0),
                "skipped_files": getattr(result, "skipped_files", 0),
                "chunk_count": getattr(result, "chunk_count", 0),
                "errors": getattr(result, "errors", []),
            }
        return {"status": "ok", "state": get_sync_state(), "result": result}
    except Exception as exc:
        with _sync_lock:
            _sync_state["running"] = False
            _sync_state["last_finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
            _sync_state["last_error"] = str(exc)
        raise
