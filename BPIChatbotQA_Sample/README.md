# BPI-IBM QA Chatbot 🧪

A **RAG-powered chatbot** named **BPI-IBM QA Chatbot** that helps SIT/UAT testers understand system behavior, user stories, and design documents — reducing invalid defects.

## Quick Start

```bash
# 1. Run document ingestion (once, or when docs change)
python ingest.py

# 2. Start the server
python backend/main.py

# 3. Open browser
# http://localhost:8000
```

Or simply double-click **`start.bat`** — it does all of the above automatically.

## Configuration

Edit [`backend/config.py`](backend/config.py) to change settings:

| Setting | Default | Description |
|---|---|---|
| `DOCS_PATH` | `"docs"` | Path to documents folder or network share |
| `LLM_MODEL` | `"mistral"` | Ollama model: `mistral`, `llama3.2`, `gemma4:e2b` |
| `CHUNK_SIZE` | `800` | Characters per document chunk |
| `TOP_K_DOCS` | `5` | Chunks retrieved per query |

### Using a Network Share Path

```python
# In backend/config.py
DOCS_PATH = r"\\SERVER\ShareName\TestDocuments"
```

Or set the environment variable:
```bash
set BPI_DOCS_PATH=\\SERVER\ShareName\TestDocuments
python ingest.py
```

## Supported Document Types
- `.pdf` — PDFs (user stories, design docs, specs)
- `.docx` — Word documents
- `.txt` / `.md` — Plain text and Markdown files

## Architecture

```
Browser (frontend/)  →  FastAPI (backend/main.py)
                            ↓
                     RAG Pipeline (rag_pipeline.py)
                       ↙          ↘
               ChromaDB          Ollama Mistral
             (vectorstore/)     (localhost:11434)
                   ↑
            Ingest (ingest.py)
                   ↑
         Share Path / Local docs
```

## Re-ingesting Documents

Whenever you add or update documents, run:
```bash
python ingest.py
# or, for a network share:
python ingest.py --path "\\SERVER\Share\Folder"
```

Then restart the backend server.

## Render Deployment with Groq

This project can be deployed to Render using the included [`render.yaml`](render.yaml).

### Required environment variables

Set these in the Render dashboard:

- `GROQ_API_KEY` — your Groq API key
- `BPI_DOCS_PATH` — already set to `/app/docs` in `render.yaml`

### Deployment notes

- Put your source documents inside the repo `docs/` folder so they are available at deploy time.
- During Render build, the app installs dependencies and runs document ingestion automatically.
- The frontend uses the same origin as the backend, so no localhost changes are needed in production.

### Local security note

Do not hardcode API keys in source code. This project now reads `GROQ_API_KEY` only from environment variables.

### Render URLs to test after deploy

- `/` — chatbot UI
- `/health` — backend health status
- `/docs` — FastAPI API docs

