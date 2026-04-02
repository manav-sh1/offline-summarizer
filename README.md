# TextForge 🛠️

TextForge is a powerful, **local-first** text processing platform that brings industrial-grade summarization, keyword extraction, and grammar analysis to your machine. It is designed for users who prioritize privacy and performance without relying on external cloud APIs.

By leveraging **FastAPI** for a high-performance backend and **Streamlit** for an intuitive user experience, TextForge provides a seamless bridge to local LLMs via **Ollama**.

---

## ✨ Key Features

- **Local Summarization**: Condense long documents into short, medium, or long formats using local Llama-based models.
- **Intelligent Keyword Extraction**: Automatically identify the most relevant themes and terms in any text.
- **Deep Grammar Check**: Analyze text for grammatical issues with contextual improvement suggestions.
- **Graceful Fallback**: If LLM services are unavailable, the system automatically switches to extractive summarization logic so you're never blocked.
- **Privacy First**: Zero data leaves your local machine.

---

## 🏗️ Tech Stack

- **Backend**: FastAPI (Python 3.10+)
- **Frontend**: Streamlit
- **LLM Engine**: Ollama (local execution)
- **Schema Validation**: Pydantic v2
- **Environment Management**: Pydantic-Settings & Dotenv

---

## 📋 Prerequisites

Before you begin, ensure your system meets the following requirements:

### Hard Requirements
- **Python**: 3.10 or higher.
- **Ollama**: Installed and running ([Download here](https://ollama.com/)).

### Hardware Recommendations (for LLM Features)
- **VRAM**: At least **2GB of dedicated VRAM** is required to run small models (like `qwen2.5:1.5b` or `llama3.2:1b`) smoothly. 
- **RAM**: 8GB+ of system memory.
- **Storage**: ~3GB of free space for model weights.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/offline-summarizer.git
cd offline-summarizer
```

### 2. Environment Setup
Create a virtual environment and install the required dependencies:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Initialize Ollama Models
Ensure Ollama is running, then pull the recommended models for TextForge:
```bash
ollama serve
ollama pull qwen2.5:1.5b
```

### 4. Configuration (Optional)
Copy the example environment file and adjust the ports or model names if needed:
```bash
cp .env.example .env
```

---

## 🛠️ Running the Application

TextForge uses a unified entry point (`main.py`) to manage both the API and the UI. You will need **two terminal windows** (or two background processes) to run the full stack locally.

### Window 1: Backend API
Starts the FastAPI server at `http://127.0.0.1:5000`.
```bash
python main.py api
```

### Window 2: Frontend UI
Starts the Streamlit interface at `http://localhost:8501`.
```bash
python main.py ui
```

---

## 📁 Architecture Overview

```text
offline-summarizer/
├── main.py              # Central entry point (CLI)
├── config.py            # Global configuration & env var mapping
├── logging_config.py    # Standardized logging setup
├── backend/
│   ├── app.py           # FastAPI application initialization
│   ├── dependencies.py  # Service injection & shared instances
│   ├── api/routes/      # Versioned REST endpoints (summarize, keywords, etc.)
│   ├── schemas/         # Pydantic models for request/response validation
│   └── services/        # Core business logic (Ollama clients, fallbacks)
└── frontend/
    ├── ui.py            # Main Streamlit application
    ├── api_client.py    # Python wrapper for internal API calls
    ├── components.py    # Reusable Streamlit UI elements
```

---

## 🔌 API Documentation

Once the backend is running, you can explore the interactive documentation at:
- **Swagger UI**: [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)
- **ReDoc**: [http://127.0.0.1:5000/redoc](http://127.0.0.1:5000/redoc)

### Core Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Check if backend and Ollama are reachable. |
| `POST` | `/api/v1/text/summarize` | Generate a summary with adjustable length. |
| `POST` | `/api/v1/text/keywords` | Extract top keywords from text. |
| `POST` | `/api/v1/text/grammar` | Detect and suggest fixes for grammar issues. |

---

## ❓ Troubleshooting

- **Ollama Connection Refused**: Ensure you have run `ollama serve` in a background terminal.
- **Slow Generation**: Ensure your machine has at least 2GB of VRAM. If it's still slow, try using a smaller model like `llama3.2:1b`.
- **Backend Unavailable in UI**: Ensure the API is running on port `5000` (the default) before launching the UI.
- **Port Conflicts**: If port `5000` or `8501` is busy, you can change them in the `.env` file.

---

## 🤝 Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
