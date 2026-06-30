# 📄 AI Resume Analyzer

A fully local, zero-cost AI-powered resume analysis tool built with Streamlit, Ollama, FAISS, and spaCy.

---

## Features

- **Resume Analyzer** — Upload a PDF or DOCX resume. Extracts contact info, skills, and all sections automatically.
- **ATS Report** — Scores your resume against a job description using a 3-part formula: Hard Skills (40%) + Semantic Profile Match (40%) + Experience & Education (20%).
- **JD Matching** — Paste any job description and get a match score, skill gap analysis, and actionable recommendations.
- **AI Resume Chat** — Ask anything about your resume using a local RAG pipeline powered by Ollama. Fully offline.
- **Interview Preparation** — Generates tailored Technical, HR, and Behavioral questions based on your resume and chosen difficulty level.
- **Cover Letter Generator** — Produces a personalized, ATS-friendly cover letter grounded strictly in your resume and the target role.
- **Settings** — Check Ollama connectivity, inspect available models, and reset session state.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Streamlit (multi-page) |
| LLM & Embeddings | Ollama (`mistral`, `nomic-embed-text`) |
| Vector Store | FAISS |
| Resume Parsing | PyMuPDF, python-docx, spaCy |
| Grammar Check | language-tool-python |
| Similarity | scikit-learn |
| Config | python-dotenv |

---

## Project Structure

```
Resume-Analyzer-AI/
├── Home.py                     # Entry point & session status dashboard
├── config.py                   # Loads env vars
├── requirements.txt
├── .env.example
│
├── pages/
│   ├── Resume_Analyzer.py
│   ├── ATS_Report.py
│   ├── _JD_Matching.py
│   ├── AI_Resume_Chat.py
│   ├── Interview_Preparation.py
│   ├── Cover_Letter_Generator.py
│   └── Settings.py
│
├── ats/                        # ATS scoring logic
│   ├── scorer.py               # 3-part scoring formula
│   ├── keyword_match.py
│   ├── grammar.py
│   └── ats_text_cleaner.py
│
├── embeddings/                 # FAISS vector store
│   ├── chunker.py
│   ├── embedder.py
│   └── faiss_db.py
│
├── llm/                        # LLM integration
│   ├── ollama_client.py
│   ├── prompts.py
│   └── rag_pipeline.py
│
├── parser/                     # Resume parsing
│   ├── pdf_parser.py
│   ├── doc_parser.py
│   ├── resume_extractor.py
│   ├── section_extractor.py
│   ├── contact_extractor.py
│   ├── skill_extractor.py
│   └── text_cleaner.py
│
├── jd_matching/
│   ├── matcher.py
│   └── similarity.py
│
├── interview/
│   └── generator.py
│
├── services/
│   ├── resume_service.py
│   └── chat_service.py
│
├── models/                     # Pydantic data models
│   ├── resume.py
│   ├── ats_report.py
│   ├── jd_report.py
│   ├── interview_report.py
│   ├── grammar_report.py
│   ├── keyword_report.py
│   ├── document_chunk.py
│   └── resume_processing_result.py
│
├── data/
│   ├── skills.json
│   ├── ats_keywords.json
│   └── stopwords.txt
│
├── faiss_index/
│   ├── index.faiss
│   └── metadata.pkl
│
└── assets/
    └── styles.css
```

---

## Setup

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Resume-Analyzer-AI.git
cd Resume-Analyzer-AI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Pull Ollama models

```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### 5. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env`:

```env
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=mistral
EMBEDDING_MODEL=nomic-embed-text
FAISS_INDEX_PATH=faiss_index/index.faiss
FAISS_METADATA_PATH=faiss_index/metadata.pkl
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE_MB=10
CHUNK_SIZE=500
CHUNK_OVERLAP=100
TOP_K_RESULTS=5
APP_TITLE=AI Resume Analyzer
```

### 6. Run the app

```bash
streamlit run Home.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

1. Go to **Resume Analyzer** and upload your PDF or DOCX resume.
2. Navigate to any feature page — all pages read from the uploaded resume automatically.
3. For ATS scoring and JD matching, paste the job description when prompted.
4. Use **AI Resume Chat** for freeform Q&A about your resume content.
5. Check **Settings** to verify Ollama is connected and switch models.

---

## Notes

- All processing is done locally. No data leaves your machine.
- The FAISS index is rebuilt automatically each time a new resume is uploaded.
- If Ollama is not running, AI features (chat, cover letter, interview questions) will be unavailable but parsing and ATS scoring will still work.

---

## License

MIT