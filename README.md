# 📝 Video Note Extractor

> **Multimodal AI system** that converts any video lecture into structured, academic-quality study notes — by simultaneously processing audio, visual frames, and on-screen text.

Built with **OpenAI Whisper · Groq LLaMA 3.3 70B · OpenCV · Tesseract OCR · Streamlit**

---

## ✨ Features

- 🎙️ **Audio transcription** — Speech-to-text using OpenAI Whisper with timestamps
- 👁️ **Visual frame analysis** — Key frame extraction every N seconds using OpenCV
- 📊 **OCR on slides** — Captures text from slides, diagrams, and whiteboards via Tesseract
- 🤖 **LLM fusion** — All modalities merged by LLaMA 3.3 70B (via Groq) into coherent notes
- 📄 **Dual export** — Download notes as Markdown or PDF
- 🌐 **Web UI** — Clean Streamlit interface, no coding needed

---

## 🏗️ System Architecture

```
 ![System Architecture](https://github.com/user-attachments/assets/e788f817-051f-4a24-830f-6b7174c12edf)


```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/video-note-extractor.git
cd video-note-extractor
```

### 2. Install system dependencies

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y ffmpeg tesseract-ocr

# macOS
brew install ffmpeg tesseract
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

Get your **FREE** Groq API key at [console.groq.com](https://console.groq.com) — no credit card required.

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔑 Getting Your Free Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key and paste it in the sidebar (or add to `.env`)

---

## 📁 Project Structure

```
video-note-extractor/
│
├── app.py                  # Streamlit web interface
├── pipeline.py             # Main orchestration pipeline
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
│
├── src/
│   ├── audio_module.py     # Whisper transcription
│   ├── vision_module.py    # Frame extraction + OCR
│   ├── llm_module.py       # Groq/LLaMA note generation
│   └── output_module.py    # MD + PDF export
│
└── outputs/                # Generated notes saved here
```

---

## ⚙️ Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| Whisper model | `base` | `tiny` / `base` / `small` / `medium` |
| Frame interval | `30s` | Extract one frame every N seconds |
| LLM model | `llama-3.3-70b-versatile` | Groq model to use |
| Output dir | `outputs/` | Where notes are saved |

---

## 🌐 Supported Video Platforms

- YouTube
- Vimeo
- Coursera (public videos)
- Dailymotion
- Any platform supported by [yt-dlp](https://github.com/yt-dlp/yt-dlp)

---

## 🧠 Research Context

This project is part of my AI / ML Internshsip at @ZYNVEX Solutions, exploring:

- **Multimodal learning** — fusion of audio, visual, and textual data streams
- **Large Language Models** — using LLaMA 3.3 for structured knowledge extraction
- **Computer Vision** — key frame detection and OCR with OpenCV + Tesseract
- **NLP** — speech recognition and text structuring with Whisper

---

## 📦 Tech Stack

| Component | Technology |
|-----------|-----------|
| Audio transcription | OpenAI Whisper |
| Video download | yt-dlp |
| Frame extraction | OpenCV |
| OCR | Tesseract + pytesseract |
| LLM | LLaMA 3.3 70B via Groq API |
| Web UI | Streamlit |
| PDF generation | fpdf2 |

---

## 👩‍💻 Author

**Rafia Rameen**
Software Engineer Student | AI / ML Intern at @ZYNVEX Solutions

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/rafia-rameen-88260a344)

---

## 📄 License

MIT License — feel free to use, modify, and build on this project.
