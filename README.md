# LogTester

A DevOps-focused AI-like log analyzer (MVP) that detects errors in Python/Java/Jenkins logs and returns a structured analysis.

## API
- `GET /health` -> health check
- `POST /analyze` -> analyze a pasted log

### Run locally
```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
