# 📄 AI Resume Analyzer & Job Matcher

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-F7931E.svg)](https://scikit-learn.org/)
[![spaCy](https://img.shields.io/badge/spaCy-3.7%2B-09A3D5.svg)](https://spacy.io/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **A production-ready student portfolio project built for software engineering placements and technical interviews.**
> Analyzes resumes, scores ATS compliance, matches skills against job postings with TF-IDF cosine similarity, and highlights skill gaps with zero paid cloud API dependencies.

---

## 🌟 Key Features

1. **📑 PyMuPDF Text Extraction**: Rapid, high-fidelity PDF and document parsing without OCR latency or third-party cloud costs.
2. **🧠 NLP Candidate & Skill Extraction**: Rule-based + Named Entity Recognition (NER) pipeline parsing contact details, links (GitHub, LinkedIn), section headers, and 100+ categorized technical skills.
3. **📊 Multi-Factor Resume Scoring**: Comprehensive 100-point scoring algorithm combining ATS compliance, technical skill repertoire, content completeness, and quantifiable impact metrics.
4. **🎯 TF-IDF Cosine Similarity Job Matching**: Employs Scikit-learn vectorization to mathematically quantify alignment between candidate resumes and job descriptions or benchmark roles.
5. **🔍 Interactive Skill Gap Analysis**: Categorizes matched competencies versus critical missing skills, accompanied by Plotly radar charts and readiness ratings.
6. **✅ Enterprise ATS Compliance Audit**: Checks section structure, contact readability, action power verbs, and numeric metric density.
7. **💾 Local SQLite Persistence**: Stores parsed candidate profiles, scan records, and benchmark roles locally with zero external configuration.

---

## 🏗️ Project Architecture

```
AI-Resume-Analyzer/
│
├── app.py                      # Main Streamlit application orchestrator
├── requirements.txt            # Production dependencies
├── README.md                   # Comprehensive documentation & interview guide
├── .gitignore                  # Git exclusions for Python and SQLite
│
├── data/                       # Curated datasets
│   ├── skills.csv              # 100+ categorized technical and soft skills
│   └── job_roles.csv           # Role benchmark dataset (skills, experience, descriptions)
│
├── database/                   # SQLite database operations
│   ├── __init__.py
│   └── database.py             # Schema initialization, CRUD, and analytics aggregation
│
├── nlp/                        # Natural Language Processing pipeline
│   ├── __init__.py
│   ├── text_cleaner.py         # Text sanitization, regex filters, tokenizers, stopword removal
│   ├── skill_extractor.py      # Dictionary and boundary matching for technical skills
│   ├── job_analyzer.py         # Extracts required/preferred skills and experience cues from JDs
│   └── resume_parser.py        # Name heuristics, NER, contact links, and section detectors
│
├── analyzer/                   # Core evaluation engines
│   ├── __init__.py
│   ├── resume_score.py         # Multi-factor 100-point scoring model
│   ├── similarity.py           # Scikit-learn TF-IDF & Cosine Similarity
│   ├── ats_checker.py          # ATS compliance checklist & action verb audit
│   └── skill_gap.py            # Matched vs missing skill discrepancy engine
│
├── utils/                      # Document readers & visualizers
│   ├── __init__.py
│   ├── pdf_reader.py           # PyMuPDF (fitz) text and page extraction
│   └── helpers.py              # Plotly chart builders (gauges, radar charts, donuts)
│
├── pages/                      # Streamlit Multi-Page application modules
│   ├── dashboard.py            # Scan analytics, recent evaluations, and role lists
│   ├── resume_analysis.py      # Detailed candidate profile, radar breakdown, and skills
│   ├── job_matcher.py          # TF-IDF cosine similarity job alignment
│   ├── skill_gap.py            # Visual skill gap & role readiness assessment
│   ├── ats_checker.py          # ATS checklist audit and actionable suggestions
│   └── recommendations.py      # Google XYZ bullet rewrites and placement roadmaps
│
└── assets/
    └── logo.png                # Application branding logo
```

---

## 🛠️ Technology Stack & Engineering Justifications

| Component | Technology | Why Chosen Over Alternatives? |
| :--- | :--- | :--- |
| **Frontend Framework** | **Streamlit** | Rapid, pure-Python UI with built-in reactive state, allowing focus on backend logic without React/Node build complexity. |
| **Machine Learning** | **Scikit-learn** | High-performance, explainable TF-IDF vectorization and cosine similarity. Computationally lightweight and fast compared to oversized neural models. |
| **NLP** | **spaCy & NLTK** | Tokenization, stopword removal, and NER entities run entirely on the local CPU without token costs or rate limits. |
| **Document Parsing** | **PyMuPDF (`fitz`)** | 10x-20x faster than PyPDF2/PDFMiner with superior font extraction and multi-page stream handling. |
| **Database** | **SQLite** | Zero-configuration, serverless, single-file relational storage with full ACID compliance for local portfolios. |
| **Data Visualizations** | **Plotly** | Clean, interactive vector charts (gauges, radar plots, donuts) rendered seamlessly in the browser. |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14 installed on your machine.
- Git installed.

### 2. Clone the Repository
```bash
git clone https://github.com/rudraptl11903/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### 3. Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Download NLP Models (One-Time Setup)
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords')"
```

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 💡 Placement & Interview Talking Points

When presenting this project in software engineering interviews, emphasize:

1. **Zero External API Dependency**:
   - The entire solution runs locally. You don't face OpenAI API costs, rate-limiting, or downtime risks during live hiring demonstrations.
2. **Explainable Mathematics vs Black-Box Models**:
   - Instead of blindly querying a prompt, the matching score uses verifiable TF-IDF term weighting and cosine geometry:
     $$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
3. **Clean Decoupled Architecture**:
   - Extraction (`utils/pdf_reader.py`), normalization (`nlp/text_cleaner.py`), analysis (`analyzer/`), and UI (`pages/`) are completely decoupled into distinct modules following single-responsibility principles.
4. **Data Privacy & Compliance**:
   - Sensitive personal resume data (names, emails, phones) is kept completely on-premise inside local SQLite, meeting modern data privacy expectations.

---

## 📄 License
This project is open-source under the MIT License.
