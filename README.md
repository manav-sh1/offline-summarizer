# TextForge

TextForge is a local-first text processing app with a production-style Python layout:

- FastAPI backend
- Streamlit frontend
- Ollama-backed summarization with fallback behavior
- Keyword extraction
- Grammar checking

## Project Structure

```text
offline-summarizer/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── backend/
│   ├── app.py
│   ├── dependencies.py
│   ├── api/routes/
│   ├── schemas/
│   └── services/
└── frontend/
    ├── api_client.py
    ├── components.py
    └── ui.py
```

## Features

- Modular services and schemas instead of single-file logic
- Versioned API routes under `/api/v1`
- One central application entry point
- Shared environment-based configuration
- Graceful degradation if Ollama is not available

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Optional but required for full LLM-powered summaries, keywords, and grammar analysis:

```bash
ollama serve
ollama pull qwen2.5:1.5b
```

4. Optional configuration:

```bash
copy .env.example .env
```

## Run

Backend:

```bash
python main.py api
```

Frontend:

```bash
python main.py ui
```

FastAPI docs:

```text
http://127.0.0.1:5000/docs
```

## API Routes

- `GET /api/v1/health`
- `POST /api/v1/text/summarize`
- `POST /api/v1/text/keywords`
- `POST /api/v1/text/grammar`

## Environment Variables

Available settings are defined in `config.py`.

- `APP_ENV`
- `API_HOST`
- `API_PORT`
- `API_BASE_PATH`
- `OLLAMA_BASE_URL`
- `OLLAMA_MODEL`
- `OLLAMA_SUMMARY_MODEL`
- `OLLAMA_KEYWORDS_MODEL`
- `OLLAMA_GRAMMAR_MODEL`
- `OLLAMA_TIMEOUT_SECONDS`
- `FRONTEND_API_URL`
- `REQUEST_TIMEOUT_SECONDS`
- `MAX_KEYWORDS`

Task-specific model overrides are optional. If unset, each feature falls back to `OLLAMA_MODEL`.

## Runtime Notes

- Summaries use Ollama when reachable and fall back to a simple extractive summary when it is not.
- Keyword extraction and grammar checking are also LLM-backed and return empty results with provider `unavailable` if Ollama is not reachable or returns invalid JSON.
- The UI talks only to the local backend and does not contain business logic.
