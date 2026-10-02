# EduGenie — Google Gemini Powered Learning Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat&logo=python)](https://python.org)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-Powered-8E75B2.svg?style=flat&logo=google)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**EduGenie** is a modern, production-quality, lightweight AI educational assistant built for students and self-learners. Powered by Google Gemini AI, EduGenie provides five core educational capabilities wrapped in a dark-first, glassmorphism web interface.

---

## 🌟 Core Capabilities

1. **Question & Answer (`POST /qa`)**: Ask academic or general educational questions and receive clear, direct, contextual answers with real-world examples.
2. **Concept Explanation (`POST /explain`)**: Enter any complex topic for a structured breakdown containing a simple definition, how it works, real-world example, key takeaways, and short recap.
3. **Interactive Quiz Generator (`POST /quiz`)**: Generates **exactly 3 multiple-choice questions (MCQs)** with **4 options per question** and **1 correct answer**. Test your knowledge interactively with immediate score feedback.
4. **Text Summarization (`POST /summarize`)**: Distills long educational text or lecture notes into revision-ready summaries with bulleted key points.
5. **Personalized Learning Path (`POST /learn/recommendations`)**: Charts a visual 3-stage roadmap (**Beginner → Intermediate → Advanced**) with topics, concepts, practical exercises, and learning resources.

---

## 🏗️ Architecture & Project Structure

EduGenie preserves a clean, lightweight architecture using FastAPI, Uvicorn, Jinja2, HTML5, CSS3, and Vanilla JavaScript.

```
c:\Users\selvadharshini\Desktop\edugeniee\
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application server & routes
│   ├── config.py            # Centralized settings & environment loader
│   ├── gemini_client.py     # Reusable Google Gemini API client abstraction
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── qna.py           # Q&A logic module
│   │   ├── explanation.py   # Concept explanation logic module
│   │   ├── quiz.py          # 3-MCQ quiz generation module with strict schema
│   │   ├── summary.py       # Summarization logic module
│   │   └── learning_path.py # 3-Stage learning path roadmap module
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── qa.py            # Pydantic request/response schemas for Q&A
│   │   ├── explanation.py   # Pydantic schemas for Explanation
│   │   ├── quiz.py          # Pydantic schemas for Quiz (3 questions, 4 options)
│   │   ├── summary.py       # Pydantic schemas for Summary
│   │   └── learning_path.py # Pydantic schemas for Learning Path
│   └── utils/
│       ├── __init__.py
│       ├── prompts.py       # System & user prompts repository
│       └── json_parser.py   # LLM output cleaner & JSON parser
├── frontend/
│   ├── templates/
│   │   └── index.html       # Single-Page web interface template
│   └── static/
│       ├── css/
│       │   └── style.css    # Glassmorphism dark-first responsive styling
│       └── js/
│           ├── api.js       # Centralized API fetch client
│           ├── quiz.js      # Interactive Quiz state machine
│           └── app.js       # Application controller & views orchestrator
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures & TestClient configuration
│   ├── test_health.py       # Health check & template rendering unit tests
│   ├── test_qa.py           # Q&A endpoint tests
│   ├── test_explain.py      # Explanation endpoint tests
│   ├── test_quiz.py         # Quiz endpoint validation tests (3 MCQs, 4 options)
│   ├── test_summarize.py    # Summary endpoint tests
│   └── test_learning_path.py# Learning path endpoint tests
├── .env                     # Local environment file (DO NOT commit secrets!)
├── .env.example             # Environment template
├── .gitignore               # Git exclusion rules
├── requirements.txt         # Python package dependencies
└── README.md                # Project documentation
```

---

## 🔒 Security Principles & Key Management

- **Zero Hardcoded Secrets**: The Google Gemini API key is **never** placed inside HTML, CSS, JS, Git commits, or public files.
- **Server-Side API Calls Only**: The browser calls FastAPI endpoints (`/qa`, `/explain`, `/quiz`, `/summarize`, `/learn/recommendations`). The frontend **never** interacts with Gemini directly.
- **Environment Isolation**: The backend reads secrets strictly from `GEMINI_API_KEY` via `python-dotenv`.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Google Gemini API Key (Get your key from [Google AI Studio](https://aistudio.google.com/))

### 1. Environment Setup

Clone or open the project folder:

```bash
cd c:\Users\selvadharshini\Desktop\edugeniee
```

Create a virtual environment:

**Windows**:
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux/macOS**:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Key

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and set your `GEMINI_API_KEY`:

```env
GEMINI_API_KEY=AIzaSy...your_actual_gemini_api_key_here
MODEL_NAME=gemini-2.5-flash
```

---

## 💻 Running EduGenie Locally

Start the Uvicorn development server:

```bash
uvicorn backend.main:app --reload
```

Open your browser and navigate to:
```
http://127.0.0.1:8000
```

---

## 📡 API Reference

### Health Check
- `GET /health`
- **Response**: `{"status": "ok"}`

### 1. Question & Answer
- `POST /qa`
- **Request Body**: `{"question": "What is photosynthesis?"}`
- **Response**: `{"answer": "..."}`

### 2. Concept Explanation
- `POST /explain`
- **Request Body**: `{"topic": "Quantum Computing"}`
- **Response**: `{"topic": "Quantum Computing", "explanation": "..."}`

### 3. Quiz Generation
- `POST /quiz`
- **Request Body**: `{"text": "Cellular respiration and mitochondria"}`
- **Response**:
  ```json
  {
    "questions": [
      {
        "question": "Where does cellular respiration occur?",
        "options": ["Mitochondria", "Nucleus", "Ribosome", "Golgi Body"],
        "answer": "Mitochondria"
      }
    ]
  }
  ```

### 4. Text Summarization
- `POST /summarize`
- **Request Body**: `{"text": "Long educational text passage..."}`
- **Response**: `{"summary": "..."}`

### 5. Learning Path Recommendations
- `POST /learn/recommendations`
- **Request Body**: `{"topic": "Machine Learning"}`
- **Response**: `{"topic": "Machine Learning", "stages": [...]}`

---

## 🧪 Running Automated Tests

Run the complete pytest test suite:

```bash
pytest -v
```

Tests validate:
- `/health` and UI template loading
- Input validation and exception handling (400, 422, 429, 500, 503)
- Strict Quiz rules (3 questions, 4 options per question, correct answer matching an option)
- Response structures for Q&A, Explanation, Summary, and Learning Path

---

## 📄 License

This project is licensed under the MIT License.
