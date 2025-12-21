from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .schemas import AnalyzeRequest, AnalyzeResponse
from .analyzer import analyze_log

app = FastAPI(title="LogTester API", version="0.1.0")

# --- Static UI (GUI) ---
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# This serves files under /static (optional, but useful)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def root():
    # Serve the GUI as the homepage
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/ui")
def ui():
    # Alternative path to the GUI
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    error_type, summary, cause, fixes, conf, extracted = analyze_log(req.log_text, req.source)
    return AnalyzeResponse(
        error_type=error_type,
        root_cause_summary=summary,
        most_likely_cause=cause,
        suggested_fixes=fixes,
        confidence=conf,
        extracted_error_lines=extracted,
    )

