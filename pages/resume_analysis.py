"""
resume_analysis.py
Detailed Resume Breakdown & Scoring page.
Extracts contact information, sections, technical skills, and evaluates resume quality.
"""

import os
import sys
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.database import init_db, save_resume, save_analysis
from utils.pdf_reader import extract_text_from_file
from nlp.resume_parser import parse_resume
from analyzer.resume_score import calculate_resume_score
from utils.helpers import (
    calculate_file_hash,
    create_gauge_chart,
    create_radar_chart,
    create_category_bar_chart,
)

st.set_page_config(page_title="Resume Analysis | AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 Detailed Resume Analysis & Scoring")
st.markdown("Inspect candidate metadata, extracted technical skills, and multidimensional resume quality breakdown.")

# Check if resume is already loaded in session state or upload new
uploaded_file = st.file_uploader(
    "Upload a Resume to Analyze (PDF, DOCX, or TXT)",
    type=["pdf", "docx", "txt"],
    key="analysis_uploader"
)

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_hash = calculate_file_hash(file_bytes)

    if st.session_state.get("current_file_hash") != file_hash:
        with st.spinner("Extracting text and running NLP parser..."):
            extracted = extract_text_from_file(uploaded_file)
            if extracted["success"]:
                parsed = parse_resume(extracted["text"], filename=uploaded_file.name)
                score_data = calculate_resume_score(parsed)
                st.session_state["resume_data"] = parsed
                st.session_state["resume_score"] = score_data
                st.session_state["current_file_hash"] = file_hash
                st.success("Resume parsed successfully!")
            else:
                st.error(f"Error extracting text: {extracted['error']}")

# Verify if resume data exists
if "resume_data" not in st.session_state or st.session_state["resume_data"] is None:
    st.info("👋 Please upload a resume above or on the Home page to begin.")
else:
    resume = st.session_state["resume_data"]
    score = st.session_state["resume_score"]

    col_meta1, col_meta2 = st.columns([2, 1])

    with col_meta1:
        st.subheader("👤 Candidate Profile")
        st.markdown(f"**Name:** `{resume['candidate_name']}`")
        st.markdown(f"**Email:** `{resume['email']}`")
        st.markdown(f"**Phone:** `{resume['phone']}`")

        links = resume.get("links", {})
        link_str = []
        if links.get("linkedin"):
            link_str.append(f"[LinkedIn]({links['linkedin']})")
        if links.get("github"):
            link_str.append(f"[GitHub]({links['github']})")
        if links.get("portfolio"):
            link_str.append(f"[Portfolio]({links['portfolio']})")

        st.markdown(f"**Links:** {' | '.join(link_str) if link_str else 'None detected'}")

    with col_meta2:
        st.plotly_chart(
            create_gauge_chart(score["overall_score"], title="Overall Score"),
            use_container_width=True
        )

    st.divider()

    # Visualizations row: Radar chart & Category Bar Chart
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        st.subheader("🕸️ Dimension Breakdown")
        breakdown = score["breakdown"]
        categories = ["ATS & Structure", "Skill Breadth", "Section Health", "Impact & Metrics"]
        # Normalize to 100-point scale for radar chart
        values = [
            (breakdown["ats_structure"] / 30.0) * 100,
            (breakdown["skill_breadth"] / 30.0) * 100,
            (breakdown["content_completeness"] / 20.0) * 100,
            (breakdown["impact_metrics"] / 20.0) * 100,
        ]
        st.plotly_chart(create_radar_chart(categories, values, title="Skill & Structure Dimensions"), use_container_width=True)

    with v_col2:
        st.subheader("📊 Skill Distribution by Domain")
        cat_skills = resume.get("skills_by_category", {})
        if cat_skills:
            st.plotly_chart(create_category_bar_chart(cat_skills), use_container_width=True)
        else:
            st.write("No categorized skills detected.")

    st.divider()

    # Extracted skills by category
    st.subheader(f"🛠️ Extracted Skills ({len(resume['skills'])} Total)")
    cat_skills = resume.get("skills_by_category", {})
    if cat_skills:
        for cat_name, skills_list in cat_skills.items():
            with st.expander(f"{cat_name} ({len(skills_list)})", expanded=True):
                st.write(", ".join([f"`{s}`" for s in skills_list]))
    else:
        st.warning("No technical skills were automatically identified in the text.")

    # Save to database button
    st.divider()
    if st.button("💾 Save Profile to Local SQLite Database"):
        resume_id = save_resume(
            filename=resume["filename"],
            candidate_name=resume["candidate_name"],
            email=resume["email"],
            phone=resume["phone"],
            raw_text=resume["raw_text"],
            page_count=1,
            file_hash=st.session_state.get("current_file_hash", "")
        )
        save_analysis(
            resume_id=resume_id,
            target_role="General Evaluation",
            overall_score=score["overall_score"],
            ats_score=score["ats_score"],
            match_percentage=score["overall_score"],
            skills_count=len(resume["skills"]),
            matched_skills=",".join(resume["skills"]),
            missing_skills=""
        )
        st.success(f"Resume profile successfully persisted with ID #{resume_id} in SQLite!")
