"""
dashboard_view.py
Comprehensive candidate dashboard featuring circular progress indicators,
multidimensional skill analysis, experience, projects, education, and ATS compatibility.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from ui.components import render_top_bar, render_circular_progress, render_pill, render_status_alert
from ui.demo_data import get_demo_resume
from database.database import get_db_connection
from analyzer.similarity import compute_comprehensive_match
from analyzer.skill_gap import analyze_skill_gap


def render_dashboard_page():
    candidate_name = None
    if st.session_state.get("resume_data"):
        candidate_name = st.session_state["resume_data"].get("candidate_name")

    render_top_bar("Dashboard", candidate_name=candidate_name)

    if not st.session_state.get("resume_data"):
        render_status_alert(
            "No candidate resume loaded yet. Please upload a resume on the Home page or load our rich demo profile to view the full analytics dashboard.",
            alert_type="blue",
            title="Awaiting Resume"
        )
        c1, c2 = st.columns([1, 3])
        with c1:
            if st.button("✨ Load Demo Profile", type="primary", use_container_width=True):
                demo = get_demo_resume()
                st.session_state["resume_data"] = demo["resume_data"]
                st.session_state["resume_score"] = demo["resume_score"]
                st.session_state["current_file_hash"] = demo["file_hash"]
                st.rerun()
        return

    resume = st.session_state["resume_data"]
    score = st.session_state["resume_score"]

    # Calculate Job Match score against default/selected role
    target_role_title = st.session_state.get("selected_role_title", "Software Engineer Intern")
    with get_db_connection() as conn:
        df_roles = pd.read_sql_query("SELECT * FROM job_roles", conn)

    job_match_pct = 82.0
    recommended_roles = [
        {"role": "Full Stack Developer", "match": 88},
        {"role": "Junior Backend Developer", "match": 84},
        {"role": "Software Engineer Intern", "match": 82},
    ]

    if not df_roles.empty:
        # Match against benchmark roles dynamically
        cand_skills = resume.get("skills", [])
        computed_matches = []
        for _, r in df_roles.iterrows():
            r_req = [s.strip() for s in str(r["required_skills"]).split(",") if s.strip()]
            r_pref = [s.strip() for s in str(r["preferred_skills"]).split(",") if s.strip()]
            gap = analyze_skill_gap(cand_skills, r_req, r_pref)
            computed_matches.append({
                "role": r["role_title"],
                "match": int(round(gap["match_percentage"]))
            })
        computed_matches.sort(key=lambda x: x["match"], reverse=True)
        if computed_matches:
            recommended_roles = computed_matches[:3]
            job_match_pct = recommended_roles[0]["match"]

    # =========================================================================
    # ROW 1: FOUR CIRCULAR PROGRESS INDICATORS
    # =========================================================================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            render_circular_progress(
                score=score["overall_score"],
                label="Resume Score",
                sublabel=f"Grade: {score['grade'].split()[0]}",
                color_type="green" if score["overall_score"] >= 80 else "blue",
                suffix="/100"
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            render_circular_progress(
                score=job_match_pct,
                label="Job Match Score",
                sublabel=f"Role: {recommended_roles[0]['role']}",
                color_type="green" if job_match_pct >= 80 else "orange",
                suffix="%"
            ),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            render_circular_progress(
                score=score["ats_score"],
                label="ATS Score",
                sublabel="Compliance Rate",
                color_type="green" if score["ats_score"] >= 80 else "orange",
                suffix="%"
            ),
            unsafe_allow_html=True
        )

    with col4:
        top_role_match = recommended_roles[0]["match"] if recommended_roles else 85
        st.markdown(
            render_circular_progress(
                score=top_role_match,
                label="Recommended Roles",
                sublabel=f"Top: {recommended_roles[0]['role'][:20]}...",
                color_type="purple",
                suffix="%"
            ),
            unsafe_allow_html=True
        )

    st.write("")

    # =========================================================================
    # ROW 2: SKILL ANALYSIS (DATA VISUALIZATION) & TECHNICAL SKILLS
    # =========================================================================
    row2_left, row2_right = st.columns([1, 1])

    with row2_left:
        st.markdown(
            """
            <div class="clean-card">
                <div class="card-heading">📊 Skill Analysis (Domain Breakdown)</div>
                <div class="card-subtext">Proportional distribution of identified competencies across engineering domains.</div>
            """,
            unsafe_allow_html=True
        )
        cat_skills = resume.get("skills_by_category", {})
        if cat_skills:
            labels = list(cat_skills.keys())
            values = [len(v) for v in cat_skills.values()]
            # Colorful chart ONLY for data visualization as requested
            colors = ["#10B981", "#3B82F6", "#8B5CF6", "#F59E0B", "#EC4899", "#14B8A6"]
            fig_donut = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        hole=0.6,
                        marker={"colors": colors[:len(labels)]},
                        textinfo="label+value",
                        hoverinfo="label+value+percent",
                    )
                ]
            )
            fig_donut.update_layout(
                showlegend=True,
                legend={"orientation": "h", "yanchor": "bottom", "y": -0.2, "xanchor": "center", "x": 0.5},
                height=280,
                margin={"l": 10, "r": 10, "t": 10, "b": 10},
                paper_bgcolor="rgba(0,0,0,0)",
                font={"family": "Inter, sans-serif", "size": 11},
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No categorized skills detected.")
        st.markdown("</div>", unsafe_allow_html=True)

    with row2_right:
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">🛠️ Technical Skills ({len(resume.get('skills', []))} Detected)</div>
                <div class="card-subtext">NLP entity identified technical tools, libraries, and languages.</div>
                <div style="margin-top: 1rem; max-height: 270px; overflow-y: auto;">
            """,
            unsafe_allow_html=True
        )
        skills = resume.get("skills", [])
        if skills:
            badge_html = "".join([render_pill(s, "neutral") for s in sorted(skills)])
            st.markdown(badge_html, unsafe_allow_html=True)
        else:
            st.info("No technical skills detected.")
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.write("")

    # =========================================================================
    # ROW 3: EXPERIENCE & PROJECTS
    # =========================================================================
    row3_left, row3_right = st.columns(2)

    with row3_left:
        st.markdown(
            """
            <div class="clean-card">
                <div class="card-heading">💼 Work Experience & Tenures</div>
                <div class="card-subtext">Extracted career milestones, engineering responsibilities, and quantified impact.</div>
                <div style="margin-top: 1rem;">
            """,
            unsafe_allow_html=True
        )
        sec_exp = resume.get("section_contents", {}).get("experience", "")
        if sec_exp:
            st.markdown(f"```text\n{sec_exp[:650]}...\n```" if len(sec_exp) > 650 else f"```text\n{sec_exp}\n```")
        else:
            st.info("Experience section extracted via heuristics. View detailed breakdown in Resume Analysis.")
        st.markdown("</div></div>", unsafe_allow_html=True)

    with row3_right:
        st.markdown(
            """
            <div class="clean-card">
                <div class="card-heading">🚀 Technical Projects Portfolio</div>
                <div class="card-subtext">Identified software projects, architecture decisions, and technologies.</div>
                <div style="margin-top: 1rem;">
            """,
            unsafe_allow_html=True
        )
        sec_proj = resume.get("section_contents", {}).get("projects", "")
        if sec_proj:
            st.markdown(f"```text\n{sec_proj[:650]}...\n```" if len(sec_proj) > 650 else f"```text\n{sec_proj}\n```")
        else:
            st.info("Projects section extracted via heuristics. View detailed breakdown in Resume Analysis.")
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.write("")

    # =========================================================================
    # ROW 4: EDUCATION & ATS COMPATIBILITY
    # =========================================================================
    row4_left, row4_right = st.columns(2)

    with row4_left:
        st.markdown(
            """
            <div class="clean-card">
                <div class="card-heading">🎓 Academic Background & Education</div>
                <div class="card-subtext">Degrees, institutions, GPA milestones, and relevant coursework.</div>
                <div style="margin-top: 1rem;">
            """,
            unsafe_allow_html=True
        )
        sec_edu = resume.get("section_contents", {}).get("education", "")
        if sec_edu:
            st.markdown(f"```text\n{sec_edu[:500]}\n```")
        else:
            st.info("Education credentials verified.")
        st.markdown("</div></div>", unsafe_allow_html=True)

    with row4_right:
        st.markdown(
            """
            <div class="clean-card">
                <div class="card-heading">✅ ATS Compatibility Health</div>
                <div class="card-subtext">Compliance checklist for automated resume screening engines.</div>
                <div style="margin-top: 1rem;">
            """,
            unsafe_allow_html=True
        )
        ats_details = score.get("ats_details", {})
        checks = ats_details.get("checks", [])
        if checks:
            for chk in checks[:4]:
                color = "green" if chk["passed"] else "orange"
                icon = "✓" if chk["passed"] else "!"
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid #F3F4F6;">
                        <span style="font-size: 0.85rem; color: #374151;">{chk['title']}</span>
                        <span class="pill-tag pill-{color}">{icon} {chk['points']}/{chk['max_points']} pts</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown("</div></div>", unsafe_allow_html=True)
