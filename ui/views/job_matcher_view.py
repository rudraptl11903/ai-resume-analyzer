"""
job_matcher_view.py
Machine Learning Job Matcher powered by Scikit-Learn TF-IDF vectorization and Cosine Similarity.
Evaluates resume against custom job descriptions or industry benchmark roles.
"""

import streamlit as st
import pandas as pd
from ui.components import render_top_bar, render_circular_progress, render_pill, render_status_alert
from ui.demo_data import get_demo_resume
from database.database import get_db_connection, save_analysis, save_resume
from analyzer.similarity import compute_comprehensive_match
from analyzer.skill_gap import analyze_skill_gap
from nlp.job_analyzer import parse_job_description


def render_job_matcher_page():
    candidate_name = None
    if st.session_state.get("resume_data"):
        candidate_name = st.session_state["resume_data"].get("candidate_name")

    render_top_bar("Job Matcher", candidate_name=candidate_name)

    if not st.session_state.get("resume_data"):
        render_status_alert(
            "Please upload a resume on the Home page or load our demo profile to evaluate job matches.",
            alert_type="blue",
            title="Awaiting Resume"
        )
        if st.button("✨ Load Demo Resume", type="primary"):
            demo = get_demo_resume()
            st.session_state["resume_data"] = demo["resume_data"]
            st.session_state["resume_score"] = demo["resume_score"]
            st.session_state["current_file_hash"] = demo["file_hash"]
            st.rerun()
        return

    resume = st.session_state["resume_data"]

    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 10px; padding: 0.85rem 1.25rem; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <span style="color: #6B7280; font-size: 0.85rem;">Active Candidate:</span>
                <span style="font-weight: 600; font-size: 0.92rem; margin-left: 6px;">{resume['candidate_name']}</span>
                <span style="color: #9CA3AF; font-size: 0.82rem; margin-left: 10px;">({len(resume['skills'])} skills detected)</span>
            </div>
            <span class="pill-tag pill-neutral">{resume['filename']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_custom, tab_benchmark = st.tabs(["✍️ Custom Job Description", "📋 Benchmark Roles Library"])

    target_title = ""
    target_description = ""
    required_skills = []
    preferred_skills = []

    with tab_custom:
        custom_role_title = st.text_input(
            "Job Title (Optional):",
            value=st.session_state.get("custom_title_input", ""),
            placeholder="e.g. Associate Backend Engineer / Full Stack Intern"
        )

        sample_btn_clicked = st.button("📋 Paste Sample Software Engineer JD", type="secondary")
        default_jd_text = ""
        if sample_btn_clicked:
            default_jd_text = (
                "We are seeking a Software Engineer Intern or Junior Developer to build robust backend APIs "
                "and microservices. Requirements: Strong experience in Python, FastAPI or Django, SQL, PostgreSQL, "
                "Git, and Data Structures & Algorithms. Preferred experience with Docker, Redis, Kubernetes, "
                "AWS, REST API design, and Unit Testing. The candidate should be self-motivated and possess "
                "excellent problem-solving capabilities."
            )

        job_desc_input = st.text_area(
            "Job Description Input Area:",
            value=default_jd_text or st.session_state.get("custom_jd_input", ""),
            height=200,
            placeholder="Paste full job description, responsibilities, technical requirements, and qualifications here..."
        )

        if job_desc_input:
            parsed_job = parse_job_description(job_desc_input)
            target_title = custom_role_title or "Target Job Posting"
            target_description = job_desc_input
            required_skills = parsed_job.get("skills", [])
            preferred_skills = []

    with tab_benchmark:
        with get_db_connection() as conn:
            df_roles = pd.read_sql_query("SELECT * FROM job_roles", conn)

        if not df_roles.empty:
            role_options = df_roles["role_title"].tolist()
            selected_title = st.selectbox("Choose Benchmark Role from Database:", role_options)
            role_row = df_roles[df_roles["role_title"] == selected_title].iloc[0]

            if not job_desc_input:  # If custom wasn't specified, use benchmark
                target_title = role_row["role_title"]
                target_description = f"{role_row['role_title']} - {role_row['category']}. {role_row['description']}. Required: {role_row['required_skills']}. Preferred: {role_row['preferred_skills']}"
                required_skills = [s.strip() for s in str(role_row["required_skills"]).split(",") if s.strip()]
                preferred_skills = [s.strip() for s in str(role_row["preferred_skills"]).split(",") if s.strip()]

            with st.expander("View Benchmark Role Requirements & Description", expanded=True):
                st.markdown(f"**Category:** {role_row['category']} | **Level:** {role_row['experience_level']}")
                st.markdown(f"**Required Skills:** {role_row['required_skills']}")
                st.markdown(f"**Preferred Skills:** {role_row['preferred_skills']}")
                st.caption(role_row["description"])

    st.write("")
    analyze_btn = st.button("🚀 Analyze Job Description", type="primary", use_container_width=True)

    if analyze_btn:
        if not target_description:
            st.error("Please paste a job description or choose a benchmark role to analyze.")
            return

        with st.spinner("Executing TF-IDF Cosine Vectorization and Skill Comparison..."):
            match_results = compute_comprehensive_match(resume["raw_text"], target_description)
            gap_results = analyze_skill_gap(resume["skills"], required_skills, preferred_skills)

            st.session_state["last_match_results"] = {
                "target_title": target_title,
                "match_results": match_results,
                "gap_results": gap_results,
                "required_skills": required_skills
            }

    # Render results if available
    if "last_match_results" in st.session_state:
        res = st.session_state["last_match_results"]
        target_title = res["target_title"]
        match_results = res["match_results"]
        gap_results = res["gap_results"]
        req_skills = res["required_skills"]

        st.markdown(f"<h3 style='font-size: 1.25rem; font-weight: 600; margin-top: 1.5rem;'>Evaluation Results: {target_title}</h3>", unsafe_allow_html=True)

        col_m1, col_m2, col_m3 = st.columns([1, 1, 2])

        with col_m1:
            st.markdown(
                render_circular_progress(
                    score=gap_results["match_percentage"],
                    label="Job Match Score",
                    sublabel=gap_results["readiness_label"],
                    color_type="green" if gap_results["match_percentage"] >= 75 else "orange",
                    suffix="%"
                ),
                unsafe_allow_html=True
            )

        with col_m2:
            st.markdown(
                render_circular_progress(
                    score=match_results["composite_match"],
                    label="TF-IDF Cosine Match",
                    sublabel="Semantic Overlap",
                    color_type="blue",
                    suffix="%"
                ),
                unsafe_allow_html=True
            )

        with col_m3:
            st.markdown(
                f"""
                <div class="clean-card">
                    <div class="card-heading">🎯 Readiness Assessment</div>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #111827; margin-top: 0.5rem;">
                        Status: <span style="color: {gap_results['readiness_color']};">{gap_results['readiness_label']}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #6B7280; margin-top: 0.4rem; line-height: 1.5;">
                        Found <strong>{len(gap_results['matched_skills'])}</strong> matched skills out of <strong>{len(req_skills)}</strong> required competencies.
                        TF-IDF vector cosine similarity indicates a <strong>{match_results['composite_match']}%</strong> content relevance.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        # Skills breakdown: Required, Matched, Missing
        c_req, c_match, c_miss = st.columns(3)

        with c_req:
            st.markdown(
                """
                <div class="clean-card">
                    <div class="card-heading">📋 Required Skills</div>
                    <div class="card-subtext">All skills extracted from the job description.</div>
                    <div style="margin-top: 0.75rem;">
                """,
                unsafe_allow_html=True
            )
            if req_skills:
                pills = "".join([render_pill(s, "neutral") for s in req_skills])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.info("No specific skills extracted from JD.")
            st.markdown("</div></div>", unsafe_allow_html=True)

        with c_match:
            st.markdown(
                f"""
                <div class="clean-card">
                    <div class="card-heading">✅ Matched Skills ({len(gap_results['matched_skills'])})</div>
                    <div class="card-subtext">Skills verified on candidate's resume.</div>
                    <div style="margin-top: 0.75rem;">
                """,
                unsafe_allow_html=True
            )
            if gap_results["matched_skills"]:
                pills = "".join([render_pill(s, "green") for s in gap_results["matched_skills"]])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.warning("No overlapping skills detected.")
            st.markdown("</div></div>", unsafe_allow_html=True)

        with c_miss:
            st.markdown(
                f"""
                <div class="clean-card">
                    <div class="card-heading">❌ Missing Skills ({len(gap_results['missing_required'])})</div>
                    <div class="card-subtext">Required skills not found in resume.</div>
                    <div style="margin-top: 0.75rem;">
                """,
                unsafe_allow_html=True
            )
            if gap_results["missing_required"]:
                pills = "".join([render_pill(s, "red") for s in gap_results["missing_required"]])
                st.markdown(pills, unsafe_allow_html=True)
            else:
                st.markdown('<span class="pill-tag pill-green">All required skills covered!</span>', unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)

        # Save to SQLite history
        st.write("")
        if st.button("💾 Save Match Run to SQLite History", type="secondary"):
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
            render_status_alert(f"Analysis saved to database history for {target_title}!", alert_type="green")
