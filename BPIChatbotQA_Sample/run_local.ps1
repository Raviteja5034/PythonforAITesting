$env:BPI_DOCS_PATH = "C:\Users\RavitejaPalakurthi\Documents\Archive"

if (-not $env:GROQ_API_KEY) {
    $secureKey = Read-Host "Enter GROQ_API_KEY" -AsSecureString
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
    try {
        $env:GROQ_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

Write-Host "==============================================="
Write-Host " BPI-IBM QA Chatbot — Local Runner"
Write-Host "==============================================="
Write-Host "Docs path: $env:BPI_DOCS_PATH"
Write-Host "Groq key: $(if ($env:GROQ_API_KEY) { 'Loaded' } else { 'Missing' })"
Write-Host ""

Write-Host "[1/2] Running ingestion..."
python ingest.py
if (-not $?) { throw "Ingestion failed." }

Write-Host "[2/2] Starting backend..."
python backend/main.py
