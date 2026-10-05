"""
recommendations_view.py
Smart Career & Resume Recommendations Page.
Shows recommended job roles with match percentages, recommended high-ROI skills,
curated learning resources, and Google XYZ-formula resume improvement suggestions.
"""

import streamlit as st
import pandas as pd
from ui.components import render_top_bar, render_circular_progress, render_pill, render_status_alert
from ui.demo_data import get_demo_resume
from database.database import get_db_connection
from analyzer.skill_gap import analyze_skill_gap


def render_recommendations_page():
    candidate_name = None
    if st.session_state.get("resume_data"):
        candidate_name = st.session_state["resume_data"].get("candidate_name")

    render_top_bar("Recommendations", candidate_name=candidate_name)

    if not st.session_state.get("resume_data"):
        render_status_alert(
            "Please upload a resume on the Home page or load our demo profile to view personalized career recommendations.",
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
    candidate_skills = resume.get("skills", [])

    # Fetch all benchmark roles and calculate matches
    with get_db_connection() as conn:
        df_roles = pd.read_sql_query("SELECT * FROM job_roles", conn)

    role_evaluations = []
    missing_skill_frequency = {}

    if not df_roles.empty:
        for _, r in df_roles.iterrows():
            r_req = [s.strip() for s in str(r["required_skills"]).split(",") if s.strip()]
            r_pref = [s.strip() for s in str(r["preferred_skills"]).split(",") if s.strip()]
            gap = analyze_skill_gap(candidate_skills, r_req, r_pref)

            for s in gap["missing_required"] + gap["missing_preferred"]:
                missing_skill_frequency[s] = missing_skill_frequency.get(s, 0) + 1

            role_evaluations.append({
                "role_id": r["role_key"],
                "role_title": r["role_title"],
                "category": r["category"],
                "experience_level": r["experience_level"],
                "match_percentage": gap["match_percentage"],
                "readiness_label": gap["readiness_label"],
                "matched_count": len(gap["matched_skills"]),
                "missing_count": len(gap["missing_required"])
            })

        role_evaluations.sort(key=lambda x: x["match_percentage"], reverse=True)

    # Sort missing skills by popularity/frequency
    top_recommended_skills = sorted(missing_skill_frequency.items(), key=lambda x: x[1], reverse=True)[:6]

    # =========================================================================
    # ROW 1: RECOMMENDED JOB ROLES & MATCH PERCENTAGE
    # =========================================================================
    st.markdown(
        """
        <div class="clean-card">
            <div class="card-heading">🎯 Recommended Job Roles & Match Percentages</div>
            <div class="card-subtext">Ranked according to technical overlap with your parsed resume profile.</div>
        """,
        unsafe_allow_html=True
    )

    if role_evaluations:
        top_roles = role_evaluations[:4]
        cols = st.columns(len(top_roles))
        for idx, r_data in enumerate(top_roles):
            with cols[idx]:
                badge_type = "green" if r_data["match_percentage"] >= 80 else ("orange" if r_data["match_percentage"] >= 65 else "neutral")
                st.markdown(
                    f"""
                    <div style="border: 1px solid #E5E7EB; border-radius: 10px; padding: 1.1rem; background: #FFFFFF; text-align: center; height: 100%;">
                        <div style="font-size: 1.5rem; font-weight: 700; color: #111827;">{int(round(r_data['match_percentage']))}%</div>
                        <div style="font-size: 0.95rem; font-weight: 600; color: #111827; margin: 4px 0;">{r_data['role_title']}</div>
                        <div style="font-size: 0.78rem; color: #6B7280; margin-bottom: 8px;">{r_data['category']} • {r_data['experience_level']}</div>
                        <span class="pill-tag pill-{badge_type}">{r_data['matched_count']} matched</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # =========================================================================
    # ROW 2: RECOMMENDED SKILLS TO LEARN NEXT
    # =========================================================================
    r2_left, r2_right = st.columns([1, 1])

    with r2_left:
        st.markdown(
            """
            <div class="clean-card">
                <div class="card-heading">⚡ High-ROI Skills to Acquire</div>
                <div class="card-subtext">Adding these competencies unlocks the highest number of targeted job opportunities.</div>
                <div style="margin-top: 1rem;">
            """,
            unsafe_allow_html=True
        )
        if top_recommended_skills:
            for skill_name, freq in top_recommended_skills:
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #F3F4F6;">
                        <span style="font-weight: 500; font-size: 0.88rem; color: #111827;">{skill_name}</span>
                        <div>
                            <span class="pill-tag pill-purple">+{freq * 4}% Match Boost</span>
                            <span class="pill-tag pill-neutral">Demand: {freq} roles</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            pills = "".join([render_pill(s, "purple") for s in ["Docker", "Kubernetes", "Redis", "TypeScript", "CI/CD"]])
            st.markdown(pills, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with r2_right:
        st.markdown(
            """
            <div class="clean-card">
                <div class="card-heading">📚 Curated Learning Resources</div>
                <div class="card-subtext">Free, industry-standard engineering roadmaps and interactive tutorials.</div>
                <div style="margin-top: 1rem; font-size: 0.88rem; line-height: 1.8;">
                    <div>• <strong>System Design Primer:</strong> <a href="https://github.com/donnemartin/system-design-primer" target="_blank" style="color: #111827; font-weight: 500;">github.com/donnemartin/system-design-primer ↗</a></div>
                    <div>• <strong>Developer Roadmaps:</strong> <a href="https://roadmap.sh" target="_blank" style="color: #111827; font-weight: 500;">roadmap.sh (Backend & DevOps) ↗</a></div>
                    <div>• <strong>Docker & Kubernetes:</strong> <a href="https://docs.docker.com/get-started/" target="_blank" style="color: #111827; font-weight: 500;">docs.docker.com/get-started ↗</a></div>
                    <div>• <strong>Redis University:</strong> <a href="https://university.redis.com/" target="_blank" style="color: #111827; font-weight: 500;">university.redis.com ↗</a></div>
                    <div>• <strong>NeetCode LeetCode 150:</strong> <a href="https://neetcode.io/practice" target="_blank" style="color: #111827; font-weight: 500;">neetcode.io/practice ↗</a></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # =========================================================================
    # ROW 3: RESUME IMPROVEMENT SUGGESTIONS (GOOGLE XYZ FORMULA)
    # =========================================================================
    st.markdown(
        """
        <div class="clean-card">
            <div class="card-heading">✍️ Resume Improvement Suggestions (The Google XYZ Formula)</div>
            <div class="card-subtext">Framework: <strong>"Accomplished [X], as measured by [Y], by doing [Z]"</strong></div>
            <div style="margin-top: 1.25rem;">
        """,
        unsafe_allow_html=True
    )

    examples = [
        {
            "role": "Backend & API Optimization",
            "weak": "Responsible for maintaining backend APIs and database queries.",
            "strong": "Architected asynchronous REST microservice using FastAPI and Redis, decreasing 95th-percentile database response latency from 480ms to 95ms for 15,000+ active users."
        },
        {
            "role": "Machine Learning & Feature Engineering",
            "weak": "Created machine learning models in Python for classification.",
            "strong": "Trained and deployed a Scikit-Learn Random Forest pipeline with automated cross-validation, improving classification precision by 24% across 250,000 records."
        },
        {
            "role": "Frontend & Web Development",
            "weak": "Worked on a web application frontend using React.",
            "strong": "Engineered responsive dashboard using React and Tailwind CSS, modularizing 14 reusable UI components and reducing initial page load bundle size by 35%."
        }
    ]

    for eg in examples:
        st.markdown(
            f"""
            <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 12px 16px; margin-bottom: 12px; background: #FFFFFF;">
                <div style="font-weight: 600; font-size: 0.88rem; color: #111827; margin-bottom: 6px;">📌 {eg['role']}</div>
                <div style="margin-bottom: 6px; font-size: 0.84rem;"><span class="pill-tag pill-red">Before (Weak)</span> <code style="color: #6B7280;">{eg['weak']}</code></div>
                <div style="font-size: 0.84rem;"><span class="pill-tag pill-green">After (Google XYZ)</span> <strong style="color: #065F46;">{eg['strong']}</strong></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div></div>", unsafe_allow_html=True)
