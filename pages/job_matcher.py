"""
job_matcher.py
Job Matching Engine powered by Scikit-Learn TF-IDF vectorization and Cosine Similarity.
Evaluates resume relevance against predefined benchmarks or custom pasted job postings.
"""

import os
import sys
import streamlit as st
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.database import get_db_connection, save_analysis, save_resume
from analyzer.similarity import compute_comprehensive_match
from analyzer.skill_gap import analyze_skill_gap
from nlp.job_analyzer import parse_job_description
from utils.helpers import create_gauge_chart, create_skills_comparison_chart

st.set_page_config(page_title="Job Matcher | AI Resume Analyzer", page_icon="🎯", layout="wide")

st.title("🎯 Machine Learning Job Matcher")
st.markdown("Quantify alignment between candidate resume and specific job roles using TF-IDF cosine similarity.")

# Check if resume is available in session state
if "resume_data" not in st.session_state or st.session_state["resume_data"] is None:
    st.warning("⚠️ No resume found in session. Please upload a resume on the **Home** or **Resume Analysis** page first.")
else:
    resume = st.session_state["resume_data"]
    st.success(f"Loaded Resume: **{resume['candidate_name']}** ({resume['filename']})")

    st.subheader("1. Select or Paste Job Criteria")
    tab_preset, tab_custom = st.tabs(["📋 Select From Role Benchmarks", "✍️ Paste Custom Job Description"])

    target_title = ""
    target_description = ""
    required_skills = []
    preferred_skills = []

    with tab_preset:
        with get_db_connection() as conn:
            df_roles = pd.read_sql_query("SELECT * FROM job_roles", conn)

        if not df_roles.empty:
            role_options = df_roles["role_title"].tolist()
            selected_title = st.selectbox("Choose a Benchmark Role:", role_options)
            role_row = df_roles[df_roles["role_title"] == selected_title].iloc[0]

            target_title = role_row["role_title"]
            target_description = f"{role_row['role_title']} - {role_row['category']} ({role_row['experience_level']}). {role_row['description']}. Required skills: {role_row['required_skills']}. Preferred skills: {role_row['preferred_skills']}"
            required_skills = [s.strip() for s in str(role_row["required_skills"]).split(",") if s.strip()]
            preferred_skills = [s.strip() for s in str(role_row["preferred_skills"]).split(",") if s.strip()]

            with st.expander("View Benchmark Role Details", expanded=False):
                st.markdown(f"**Category:** {role_row['category']} | **Experience Level:** {role_row['experience_level']}")
                st.markdown(f"**Required Skills:** {', '.join(required_skills)}")
                st.markdown(f"**Preferred Skills:** {', '.join(preferred_skills)}")
                st.markdown(f"**Description:** {role_row['description']}")

    with tab_custom:
        custom_role_title = st.text_input("Job Title:", placeholder="e.g. Associate Backend Engineer")
        custom_job_text = st.text_area(
            "Paste Full Job Description Here:",
            height=180,
            placeholder="Paste responsibilities, qualifications, and requirements..."
        )
        if custom_job_text:
            parsed_job = parse_job_description(custom_job_text)
            target_title = custom_role_title or "Custom Job Posting"
            target_description = custom_job_text
            required_skills = parsed_job["skills"]
            preferred_skills = []

    # Run Match Evaluation
    st.divider()
    if st.button("🚀 Calculate ML Job Match", type="primary"):
        if not target_description:
            st.error("Please select a target role or paste a job description.")
        else:
            with st.spinner("Computing TF-IDF cosine similarity & skill alignment..."):
                match_results = compute_comprehensive_match(resume["raw_text"], target_description)
                gap_results = analyze_skill_gap(resume["skills"], required_skills, preferred_skills)

                st.subheader(f"📊 Match Results for: {target_title}")

                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    st.plotly_chart(
                        create_gauge_chart(match_results["composite_match"], title="TF-IDF Cosine Match"),
                        use_container_width=True
                    )
                with col_res2:
                    st.plotly_chart(
                        create_gauge_chart(gap_results["match_percentage"], title="Skill Requirement Match"),
                        use_container_width=True
                    )
                with col_res3:
                    st.plotly_chart(
                        create_skills_comparison_chart(
                            len(gap_results["matched_skills"]),
                            len(gap_results["missing_required"] + gap_results["missing_preferred"])
                        ),
                        use_container_width=True
                    )

                st.markdown(f"### Readiness Assessment: <span style='color:{gap_results['readiness_color']}; font-weight:bold;'>{gap_results['readiness_label']}</span>", unsafe_allow_html=True)

                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    st.success(f"**Matched Skills ({len(gap_results['matched_skills'])})**")
                    if gap_results["matched_skills"]:
                        st.write(", ".join([f"`{s}`" for s in gap_results["matched_skills"]]))
                    else:
                        st.write("No matching skills found.")

                with col_m2:
                    st.error(f"**Missing Required Skills ({len(gap_results['missing_required'])})**")
                    if gap_results["missing_required"]:
                        st.write(", ".join([f"`{s}`" for s in gap_results["missing_required"]]))
                    else:
                        st.write("No missing required skills! Excellent fit.")

                # Save match run to SQLite
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
                    target_role=target_title,
                    overall_score=match_results["composite_match"],
                    ats_score=st.session_state.get("resume_score", {}).get("ats_score", 80),
                    match_percentage=gap_results["match_percentage"],
                    skills_count=len(gap_results["matched_skills"]),
                    matched_skills=",".join(gap_results["matched_skills"]),
                    missing_skills=",".join(gap_results["missing_required"])
                )
                st.toast("Evaluation saved to SQLite history!", icon="💾")
