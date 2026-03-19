# 🛠️ Python AI Toolkit

A suite of 4 offline-first AI desktop tools for writers, researchers, and teachers.
All tools share a common NLP module and run 100% locally — no cloud API required.

---

## 📦 Tools Overview

| File | Tool | What it does |
|------|------|-------------|
| `nlp_utils.py` | Shared NLP Module | Keywords, summaries, Ollama, KeyBERT — imported by all scripts |
| `ai_file_organizer_pro.py` | AI File Organizer Pro | Sorts files into folders using a local AI model |
| `audio2txt.py` | Audio → Text Transcriber | Transcribes audio/video to Markdown with summary |
| `pdf2txtv2.py` | PDF & Image OCR Engine | Extracts text from PDFs and scanned images |
| `webscrapper.py` | Web Search + Scraper | Searches DuckDuckGo, scrapes pages, exports to Markdown |

---

## 🖥️ Screenshots

> Dark-themed PyQt6 / Tkinter UIs. All tools run as standalone desktop apps.

---

## ⚙️ Requirements

### Install all dependencies at once

```bash
pip install PyQt6 transformers torch accelerate pymupdf python-docx \
            optimum-intel openvino yt-dlp keybert requests beautifulsoup4 \
            pandas duckduckgo-search pdfplumber pytesseract pillow \
            pyspellchecker surya-ocr marker-pdf
```

### Restore NVIDIA GPU support (if you have a CUDA GPU)

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### Optional external tools

| Tool | Required by | Download |
|------|-------------|----------|
| FFmpeg | `audio2txt.py` | https://ffmpeg.org/download.html |
| Tesseract OCR | `pdf2txtv2.py` | https://github.com/UB-Mannheim/tesseract/wiki |
| Ollama | All (optional) | https://ollama.com |

---

## 🚀 Quick Start

> `nlp_utils.py` **must be in the same folder** as all other scripts before running.

```bash
python ai_file_organizer_pro.py   # File organiser
python audio2txt.py               # Transcriber
python pdf2txtv2.py               # PDF / OCR engine
python webscrapper.py             # Web scraper
```

---

## 🔧 Tool Details

### 1. `ai_file_organizer_pro.py` — AI File Organizer Pro

Scans a folder of documents and uses a local HuggingFace language model to decide which subfolder each file belongs in. No cloud, no API key.

**Features:**
- PyQt6 dark-theme UI
- Supports `.txt` `.md` `.pdf` `.docx` `.csv` `.json` `.log`
- Model selector (Qwen, Llama, or custom local folder)
- Progress bar, stop button, stats panel, log export
- Duplicate file protection
- Uses existing destination folders when names match

**Models it can use (auto-downloaded on first run):**
- `Qwen/Qwen2.5-1.5B-Instruct` (lightweight, fast)
- `Qwen/Qwen2.5-3B-Instruct` (better quality)
- `meta-llama/Llama-3.2-1B-Instruct`
- Any custom local model folder

---

### 2. `audio2txt.py` — Audio/Video Transcriber Engine v5.2

Transcribes any audio or video file to a clean Markdown document with summary and keywords.

**Features:**
- Three transcription engines: faster-whisper (NVIDIA), openai-whisper (CPU), Intel OpenVINO
- YouTube download and transcribe in one click (via yt-dlp)
- Live microphone recording with InputStream callback (fixed crash)
- Batch folder processing
- Noise reduction via FFmpeg
- Ollama AI summary + KeyBERT keyword extraction
- Outputs `.md` files with tags, summary, and full transcript

**Supported input formats:** `.mp3` `.mp4` `.wav` `.m4a` `.mkv` `.ogg` `.webm` `.mov` `.avi` `.flac`

---

### 3. `pdf2txtv2.py` — Document & OCR Engine v5.1

Extracts text from PDFs and scanned images, cleans it up, and saves it as formatted Markdown.

**Features:**
- Three OCR engines: Tesseract, Surya, or Tesseract-with-Surya-fallback
- AI-powered PDF extraction via marker-pdf
- Grammar correction via PySpellChecker
- Ollama AI summary + KeyBERT keywords
- Single file and batch folder modes
- Auto-detects scanned PDFs and routes to OCR

**Supported input:** `.pdf` `.png` `.jpg` `.jpeg`

---

### 4. `webscrapper.py` — Web Search + Mega Scraper

Searches DuckDuckGo, scrapes the result pages, and saves everything as organised Markdown files with a pandas index.

**Features:**
- Automatic DuckDuckGo search (no API key needed)
- Batch URL mode — paste a `.txt` or `.csv` list of URLs
- PDF detection and download
- Link following with configurable depth
- Ollama AI summary + KeyBERT keywords per page
- Exports `scrape_index.csv` with title, URL, summary, keywords

---

### 5. `nlp_utils.py` — Shared NLP Module

Central module imported by all four tools. No need to run this directly.

**Provides:**
- `extract_keywords()` — frequency-based keyword extraction
- `pure_python_summarize()` — extractive summarisation (no model needed)
- `clean_grammar()` — spell correction via PySpellChecker
- `check_ollama_running()` — ping local Ollama server
- `ollama_summarize()` — send text to Ollama REST API
- `get_ollama_models()` — list installed Ollama models
- `keybert_keywords()` — semantic keyword extraction via KeyBERT

---

## 📁 Folder Structure

```
python_toolkit/
├── nlp_utils.py                 ← shared, required by all
├── ai_file_organizer_pro.py
├── audio2txt.py
├── pdf2txtv2.py
├── webscrapper.py
└── README.md
```

---

## 🔑 Notes

- All models download automatically from HuggingFace on first run and cache locally.
- Ollama is optional — all tools fall back to pure-Python NLP if Ollama is not running.
- Intel OpenVINO in `audio2txt.py` requires an Intel GPU; falls back to CPU automatically.
- The `marker-pdf` package pulls in the Anthropic, OpenAI, and Google SDKs as dependencies — these are only used by marker-pdf internally, not by these scripts.

---

## 📄 License

CC0-1.0 — Public Domain. Use freely for any purpose.
