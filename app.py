"""
app.py
Main entry point for AI Resume Analyzer & Job Matcher.
A production-quality student portfolio project built with Python, Streamlit,
scikit-learn, spaCy/NLTK, PyMuPDF, and SQLite.
"""

import os
import sys
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.database import init_db, load_default_roles_if_empty, get_analytics_summary
from utils.pdf_reader import extract_text_from_file
from nlp.resume_parser import parse_resume
from analyzer.resume_score import calculate_resume_score
from utils.helpers import calculate_file_hash

# Configure Streamlit page
st.set_page_config(
    page_title="AI Resume Analyzer & Job Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design System (CSS)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.25);
    }
    
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .main-subtitle {
        font-size: 1.05rem;
        color: #C7D2FE;
        line-height: 1.6;
        max-width: 800px;
    }
    
    .badge-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        color: #EEF2FF;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 6px;
        margin-top: 8px;
    }
    
    .feature-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.4rem;
        height: 100%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -5px rgba(0,0,0,0.08);
        border-color: #CBD5E1;
    }
    
    .card-icon {
        font-size: 1.8rem;
        margin-bottom: 0.6rem;
    }
    
    .card-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 0.4rem;
    }
    
    .card-desc {
        font-size: 0.88rem;
        color: #64748B;
        line-height: 1.5;
    }
    
    .metric-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #4F46E5;
    }
    
    .metric-label {
        font-size: 0.82rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 500;
        margin-top: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def initialize_app_state():
    """Initializes database schema and session state variables."""
    # SQLite schema and default benchmarks
    init_db()
    load_default_roles_if_empty()

    # Session state variables
    if "resume_data" not in st.session_state:
        st.session_state["resume_data"] = None
    if "resume_score" not in st.session_state:
        st.session_state["resume_score"] = None
    if "current_file_hash" not in st.session_state:
        st.session_state["current_file_hash"] = None
    if "selected_role_id" not in st.session_state:
        st.session_state["selected_role_id"] = "swe_intern"


def main():
    initialize_app_state()

    # Hero Banner
    st.markdown(
        """
        <div class="main-header">
            <div class="main-title">📄 AI Resume Analyzer & Job Matcher</div>
            <div class="main-subtitle">
                An intelligent candidate evaluation engine engineered for student portfolios.
                Performs deep text extraction, ATS compliance audits, TF-IDF cosine similarity job matching,
                and actionable skill gap recommendations without relying on paid APIs.
            </div>
            <div>
                <span class="badge-tag">⚡ Python 3.14</span>
                <span class="badge-tag">📊 Scikit-Learn TF-IDF</span>
                <span class="badge-tag">🧠 spaCy & NLTK</span>
                <span class="badge-tag">📑 PyMuPDF</span>
                <span class="badge-tag">💾 Local SQLite</span>
                <span class="badge-tag">📈 Plotly Visualizations</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar overview & system status
    with st.sidebar:
        logo_path = os.path.join(PROJECT_ROOT, "assets", "logo.png")
        if os.path.exists(logo_path):
            st.image(logo_path, width=200)

        st.subheader("Navigation")
        st.info("Use the sidebar pages to navigate through the modules.")

        st.divider()
        st.subheader("System Status")
        st.success("🟢 SQLite Database Connected")
        st.success("🟢 NLP Engine Online")
        st.success("🟢 ML Vectorizer Ready")

        analytics = get_analytics_summary()
        st.divider()
        st.subheader("Global Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Scans", analytics["total_scans"])
        with col2:
            st.metric("Avg Score", f"{analytics['avg_score']}%")

    # Main dashboard section
    st.subheader("🚀 Quick Start: Upload & Analyze Your Resume")
    uploaded_file = st.file_uploader(
        "Upload your resume (PDF, DOCX, or TXT)",
        type=["pdf", "docx", "txt"],
        help="Upload a resume document to trigger text parsing, skill identification, and scoring."
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_hash = calculate_file_hash(file_bytes)

        # Check if new file uploaded or already in state
        if st.session_state["current_file_hash"] != file_hash:
            with st.spinner("Analyzing resume text with PyMuPDF and NLP pipeline..."):
                extracted = extract_text_from_file(uploaded_file)
                if not extracted["success"]:
                    st.error(f"Error reading file: {extracted['error']}")
                else:
                    raw_text = extracted["text"]
                    parsed = parse_resume(raw_text, filename=uploaded_file.name)
                    score_data = calculate_resume_score(parsed)

                    st.session_state["resume_data"] = parsed
                    st.session_state["resume_score"] = score_data
                    st.session_state["current_file_hash"] = file_hash
                    st.success("✅ Resume successfully parsed and analyzed!")

    # Display resume snapshot if loaded
    if st.session_state["resume_data"] is not None:
        data = st.session_state["resume_data"]
        score = st.session_state["resume_score"]

        st.markdown("### 📋 Candidate Profile Snapshot")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value">{score['overall_score']}</div>
                    <div class="metric-label">Resume Score ({score['grade']})</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m2:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value">{score['ats_score']}%</div>
                    <div class="metric-label">ATS Compliance</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m3:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value">{len(data['skills'])}</div>
                    <div class="metric-label">Skills Detected</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_m4:
            st.markdown(
                f"""
                <div class="metric-box">
                    <div class="metric-value">{data['word_count']}</div>
                    <div class="metric-label">Total Words</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(f"**Candidate:** `{data['candidate_name']}` | **Email:** `{data['email']}` | **Phone:** `{data['phone']}`")
        st.info("👉 Navigate to **Resume Analysis**, **Job Matcher**, or **Skill Gap** from the sidebar to explore deep insights!")

    st.divider()

    # Modular Features Grid
    st.subheader("📦 Architecture & Core Modules")
    row1_c1, row1_c2, row1_c3 = st.columns(3)

    with row1_c1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="card-icon">📊</div>
                <div class="card-title">1. Dashboard</div>
                <div class="card-desc">
                    Comprehensive overview of past scans, score distributions, and recruitment pipeline statistics stored locally in SQLite.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with row1_c2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="card-icon">📄</div>
                <div class="card-title">2. Resume Analysis</div>
                <div class="card-desc">
                    Deep structural parsing using PyMuPDF and NLP entity heuristics to extract contact info, education, and categorized skills.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with row1_c3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="card-icon">🎯</div>
                <div class="card-title">3. Job Matcher</div>
                <div class="card-desc">
                    Machine learning text comparison powered by Scikit-Learn TF-IDF vectorization and cosine similarity against target job postings.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    row2_c1, row2_c2, row2_c3 = st.columns(3)

    with row2_c1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="card-icon">🔍</div>
                <div class="card-title">4. Skill Gap Analysis</div>
                <div class="card-desc">
                    Interactive radar charts and domain breakdowns highlighting matched proficiencies vs. critical missing skills for any role.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with row2_c2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="card-icon">✅</div>
                <div class="card-title">5. ATS Checker</div>
                <div class="card-desc">
                    Rigorous ATS rule audits verifying section presence, contact data, strong action verbs, and quantifiable achievement metrics.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with row2_c3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="card-icon">💡</div>
                <div class="card-title">6. Recommendations</div>
                <div class="card-desc">
                    Actionable bullet point rewrites, interview preparation tips, and prioritized learning roadmaps to land tech placements.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
