from fastapi import FastAPI
from .schemas import AnalyzeRequest, AnalyzeResponse
from .analyzer import analyze_log

app = FastAPI(title="LogTester API", version="0.1.0")


@app.get("/")
def root():
    return {
        "name": "LogTester API",
        "docs": "/docs",
        "health": "/health",
        "analyze": "/analyze"
    }


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

