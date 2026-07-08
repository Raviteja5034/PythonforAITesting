"""
main_cloud.py — Entry point for cloud deployment (Render.com)
Differences from main.py:
  - DOCS_PATH points to /app/docs (cloud folder, not local Windows path)
  - Watcher disabled (no file system events on cloud — use /ingest endpoint instead)
  - Port read from $PORT environment variable (Render requirement)
  - Uvicorn started directly
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

# Override DOCS_PATH for cloud before importing config
os.environ.setdefault("BPI_DOCS_PATH", "/app/docs")

from main import app   # re-use the same FastAPI app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("backend.main_cloud:app", host="0.0.0.0", port=port, reload=False)
