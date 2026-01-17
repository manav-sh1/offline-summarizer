# TextForge - Offline Text Summarizer

A powerful, privacy-focused desktop application for text analysis and summarization. Runs completely offline using Mistral AI, with features for keyword extraction, query-based summarization, and grammar checking.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## Features

✨ **Core Features**
- 📋 **Text Summarization** - Generate concise summaries in 3 different lengths (short, medium, long)
- 🎯 **Query-Based Summarization** - Focus summaries on specific topics or questions
- 🏷️ **Keyword Extraction** - Automatically extract important keywords using frequency analysis
- ✏️ **Grammar Checking** - Detect and suggest corrections for grammar issues
- 🔒 **100% Offline** - No data sent to external servers, complete privacy

🎨 **User Experience**
- Clean, modern dark-themed interface
- No chat history or data persistence between sessions
- Real-time processing feedback
- Responsive design that works on all screen sizes
- One-click copy functionality

⚡ **Technical**
- **FastAPI** backend with async processing
- **Streamlit** frontend for easy deployment
- **Mistral AI** via Ollama for lightweight LLM inference
- **Language Tool** for grammar checking
- **LangChain** for AI chain orchestration

## Requirements

- **Python** 3.8 or higher
- **Ollama** (for running Mistral locally)
- 8GB+ RAM recommended
- 10GB+ disk space (for Mistral model)

## Installation

### 1. Install Ollama

Download and install Ollama from [https://ollama.ai](https://ollama.ai)

After installation, pull the Mistral model:
```bash
ollama pull mistral
```

### 2. Clone or Download TextForge

```bash
git clone https://github.com/yourusername/textforge.git
cd textforge
```

### 3. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### Step 1: Start Ollama

Open a terminal and run:
```bash
ollama serve
```

This keeps Ollama running in the background. You should see:
```
listening on 127.0.0.1:11434
```

### Step 2: Start FastAPI Backend

Open a new terminal and run:
```bash
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:5000
```

### Step 3: Launch Streamlit Frontend

Open another terminal and run:
```bash
streamlit run ui.py
```

Streamlit will automatically open in your browser at `http://localhost:8501`

## Usage

### Basic Summarization

1. Paste or type text in the input area
2. Select summary length (Short/Medium/Long)
3. Click **Summarize** button
4. View results instantly

### Query-Based Summarization

1. Enter your text
2. (Optional) Add a focus query like "benefits of AI" or "climate change impacts"
3. Click **Summarize**
4. Get a summary focused on your specific query

### Extract Keywords

1. Input your text
2. Click **Keywords** button
3. View extracted important terms
4. Use for content tagging or topic identification

### Check Grammar

1. Paste your text
2. Click **Grammar** button
3. Review detected issues
4. View suggestions for corrections

## Project Structure

```
textforge/
├── app.py                 # FastAPI backend application
├── ui.py                  # Streamlit frontend application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .gitignore           # Git ignore file
```

## How It Works

### Architecture

```
User Interface (Streamlit)
        ↓
   HTTP Requests
        ↓
FastAPI Backend (Port 5000)
        ↓
LangChain + Ollama
        ↓
Mistral Model (Running Locally)
```

### Processing Pipeline

**Summarization:**
- Text is sent to FastAPI backend
- LangChain creates a prompt with user-specified length
- Mistral processes and generates summary
- Result returned to frontend

**Keyword Extraction:**
- Text is tokenized and filtered
- Stop words removed
- Word frequencies calculated
- Top keywords by frequency returned

**Grammar Checking:**
- Text analyzed by Language Tool
- Grammar issues detected with positions
- Suggestions provided where available

## Configuration

### Modify Summary Lengths

Edit in `app.py`:
```python
length_map = {'short': '2-3', 'medium': '3-5', 'long': '5-8'}
```

### Change API Port

In `app.py`:
```python
uvicorn.run(app, host="127.0.0.1", port=5000)  # Change port here
```

In `ui.py`:
```python
API_URL = "http://localhost:5000/api"  # Update port here
```

### Adjust Number of Keywords

In `ui.py`, the keywords function:
```python
keywords = extract_keywords(input_text, 8)  # Change 8 to desired number
```

## Troubleshooting

### "API Connection Failed"

**Problem:** Streamlit shows connection error
**Solution:**
1. Verify Ollama is running: `ollama serve`
2. Check FastAPI is running: `python app.py`
3. Ensure port 5000 is not in use: `lsof -i :5000` (macOS/Linux)

### "Ollama/Mistral not available"

**Problem:** Backend can't find Mistral model
**Solution:**
```bash
ollama pull mistral
# Wait for download to complete (usually 10-20 minutes)
```

### "Request timed out"

**Problem:** Summarization takes too long
**Solution:**
1. Try with shorter text
2. Increase timeout in `ui.py` (default 60 seconds)
3. Reduce summary length requirement
4. Ensure no other intensive processes running

### "Port already in use"

**Problem:** Port 5000 or 8501 already occupied
**Solution:**
```bash
# Change port in app.py
uvicorn.run(app, host="127.0.0.1", port=5001)

# Change Streamlit port
streamlit run ui.py --server.port 8502
```

### Grammar checker not working

**Problem:** Language Tool errors
**Solution:**
```bash
# Reinstall language-tool-python
pip uninstall language-tool-python
pip install language-tool-python
```

## Performance Tips

- **First run is slower**: Mistral model loads into memory (takes 10-30 seconds)
- **Optimize text length**: Shorter inputs = faster processing
- **Use Short summaries**: Faster than long summaries
- **Close other apps**: Free up RAM for Ollama

## Privacy & Security

🔐 **Complete Privacy**
- All processing happens locally on your machine
- No internet connection required
- No data collection or telemetry
- No cloud API calls
- No data logs or history

## Limitations

- First summarization request takes longer (model loading)
- Works best with English text
- Grammar checking limited to English
- Requires Mistral model download (~4GB)
- Summarization quality depends on input text clarity

## Future Enhancements

- [ ] Multi-language support
- [ ] Custom Mistral parameters (temperature, top-k)
- [ ] Batch file processing
- [ ] Export summaries (PDF, TXT, DOCX)
- [ ] Themes customization
- [ ] Advanced NLP features
- [ ] Token usage statistics
- [ ] Keyboard shortcuts

## Desktop Application Packaging

### Windows (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed app.py
pyinstaller --onefile --windowed ui.py
```

### macOS (DMG)

```bash
pip install py2app
py2app -A app.py
```

### Linux (AppImage)

```bash
pip install appimage-builder
appimage-builder --recipe AppImageBuilder.yml
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Acknowledgments

- [Mistral AI](https://mistral.ai/) - Powerful open-source LLM
- [Ollama](https://ollama.ai/) - Easy local model deployment
- [LangChain](https://langchain.com/) - LLM chain orchestration
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python API framework
- [Streamlit](https://streamlit.io/) - Rapid Python app development
- [Language Tool](https://www.languagetool.org/) - Grammar checking

**Made with ❤️ for privacy-conscious users**

Last Updated: January 2026