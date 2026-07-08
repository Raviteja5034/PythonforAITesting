@echo off
echo ================================================
echo   BPI-IBM QA Chatbot — Startup Script
echo ================================================
echo.

REM Step 1: Check Ollama is running
echo [1/3] Checking Ollama...
ollama list >nul 2>&1
if errorlevel 1 (
    echo ERROR: Ollama is not running. Please start Ollama first.
    pause
    exit /b 1
)
echo       Ollama OK

REM Step 2: Check if vector store needs ingestion
echo [2/3] Checking vector store...
if not exist "vectorstore\chroma.sqlite3" (
    echo       No documents found in vector store.
    echo       Running ingestion from 'docs' folder...
    python ingest.py
    if errorlevel 1 (
        echo ERROR: Ingestion failed. Check the output above.
        pause
        exit /b 1
    )
) else (
    echo       Vector store found — skipping ingestion.
    echo       To re-ingest, run: python ingest.py
)

REM Step 3: Start backend server
echo [3/3] Starting backend server...
echo.
echo ================================================
echo   Open your browser at: http://localhost:8000
echo   Press Ctrl+C to stop the server
echo ================================================
echo.
python backend/main.py
pause
