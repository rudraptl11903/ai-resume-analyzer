"""
skill_gap_view.py
Interactive Skill Gap Analyzer page.
Visualizes skills comparison graph, current skills, required skills,
missing skills, and personalized engineering learning paths.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from ui.components import render_top_bar, render_circular_progress, render_pill, render_status_alert
from ui.demo_data import get_demo_resume
from database.database import get_db_connection
from analyzer.skill_gap import analyze_skill_gap


def render_skill_gap_page():
    candidate_name = None
    if st.session_state.get("resume_data"):
        candidate_name = st.session_state["resume_data"].get("candidate_name")

    render_top_bar("Skill Gap", candidate_name=candidate_name)

    if not st.session_state.get("resume_data"):
        render_status_alert(
            "Please upload a resume on the Home page or load our demo profile to evaluate skill gaps.",
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

    with get_db_connection() as conn:
        df_roles = pd.read_sql_query("SELECT * FROM job_roles", conn)

    role_options = df_roles["role_title"].tolist() if not df_roles.empty else []
    selected_role_title = st.selectbox(
        "Select Target Role for Gap Analysis:",
        role_options,
        index=0 if role_options else None
    )

    if not selected_role_title:
        st.warning("No roles available in database.")
        return

    role_row = df_roles[df_roles["role_title"] == selected_role_title].iloc[0]
    req_skills = [s.strip() for s in str(role_row["required_skills"]).split(",") if s.strip()]
    pref_skills = [s.strip() for s in str(role_row["preferred_skills"]).split(",") if s.strip()]

    gap = analyze_skill_gap(candidate_skills, req_skills, pref_skills)

    # =========================================================================
    # ROW 1: SUMMARY METRICS & SKILLS COMPARISON GRAPH
    # =========================================================================
    r1_col1, r1_col2 = st.columns([1, 2])

    with r1_col1:
        st.markdown(
            render_circular_progress(
                score=gap["match_percentage"],
                label="Role Preparedness",
                sublabel=gap["readiness_label"],
                color_type="green" if gap["match_percentage"] >= 75 else "orange",
                suffix="%"
            ),
            unsafe_allow_html=True
        )

    with r1_col2:
        # Skills Comparison Graph (Bar chart comparing Matched, Missing Required, Missing Preferred)
        categories = ["Matched Skills", "Missing Required", "Missing Preferred"]
        counts = [len(gap["matched_skills"]), len(gap["missing_required"]), len(gap["missing_preferred"])]
        # Colors only for data visualization
        colors = ["#10B981", "#EF4444", "#F59E0B"]

        fig_comp = go.Figure(
            go.Bar(
                x=categories,
                y=counts,
                marker={"color": colors, "cornerradius": 6},
                text=counts,
                textposition="auto",
            )
        )
        fig_comp.update_layout(
            title={"text": "<b>Skills Comparison Breakdown</b>", "font": {"size": 15, "color": "#111827", "family": "Inter"}},
            yaxis_title="Count",
            height=240,
            margin={"l": 20, "r": 20, "t": 40, "b": 20},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"family": "Inter, sans-serif"},
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    st.write("")

    # =========================================================================
    # ROW 2: CURRENT SKILLS, REQUIRED SKILLS, MISSING SKILLS
    # =========================================================================
    c_cur, c_req, c_miss = st.columns(3)

    with c_cur:
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">👤 Current Skills ({len(candidate_skills)})</div>
                <div class="card-subtext">Competencies verified from your resume.</div>
                <div style="margin-top: 0.75rem; max-height: 250px; overflow-y: auto;">
            """,
            unsafe_allow_html=True
        )
        if candidate_skills:
            pills = "".join([render_pill(s, "neutral") for s in sorted(candidate_skills)])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.info("No skills detected.")
        st.markdown("</div></div>", unsafe_allow_html=True)

    with c_req:
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">📋 Required Skills ({len(req_skills)})</div>
                <div class="card-subtext">Baseline industry criteria for {selected_role_title}.</div>
                <div style="margin-top: 0.75rem; max-height: 250px; overflow-y: auto;">
            """,
            unsafe_allow_html=True
        )
        if req_skills:
            pills = "".join([render_pill(s, "neutral") for s in req_skills])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.info("No requirements listed.")
        st.markdown("</div></div>", unsafe_allow_html=True)

    with c_miss:
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">❌ Missing Skills ({len(gap['missing_required']) + len(gap['missing_preferred'])})</div>
                <div class="card-subtext">Priority gaps needed to increase screening pass rate.</div>
                <div style="margin-top: 0.75rem; max-height: 250px; overflow-y: auto;">
            """,
            unsafe_allow_html=True
        )
        all_missing = gap["missing_required"] + gap["missing_preferred"]
        if all_missing:
            pills = ""
            for s in gap["missing_required"]:
                pills += render_pill(f"{s} (Required)", "red")
            for s in gap["missing_preferred"]:
                pills += render_pill(f"{s} (Preferred)", "orange")
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.markdown('<span class="pill-tag pill-green">Zero skill gaps! You meet all listed requirements.</span>', unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.write("")

    # =========================================================================
    # ROW 3: RECOMMENDED LEARNING PATH
    # =========================================================================
    st.markdown(
        f"""
        <div class="clean-card">
            <div class="card-heading">🗺️ Recommended Learning Path for {selected_role_title}</div>
            <div class="card-subtext">Curated, structured milestone roadmaps to bridge critical missing competencies.</div>
        """,
        unsafe_allow_html=True
    )

    missing_list = gap["missing_required"] if gap["missing_required"] else gap["missing_preferred"]
    if not missing_list:
        missing_list = ["Docker", "Kubernetes", "Redis", "System Design"]

    top_missing_focus = missing_list[:3]

    st.markdown(
        f"""
        <div style="margin-top: 1.25rem; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px;">
            <div style="border: 1px solid #E5E7EB; border-radius: 10px; padding: 1.1rem; background: #FFFFFF;">
                <div style="font-size: 0.76rem; font-weight: 600; text-transform: uppercase; color: #8B5CF6; letter-spacing: 0.05em;">Step 1 • High Priority</div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #111827; margin: 4px 0 8px 0;">{top_missing_focus[0] if len(top_missing_focus) > 0 else 'System Architecture'}</div>
                <div style="font-size: 0.84rem; color: #6B7280; line-height: 1.5;">
                    Master core fundamentals, architecture lifecycle, syntax, and containerized microservices integration.
                </div>
                <div style="margin-top: 10px;">
                    <span class="pill-tag pill-purple">Est: 1-2 Weeks</span>
                    <span class="pill-tag pill-neutral">Hands-on Lab</span>
                </div>
            </div>

            <div style="border: 1px solid #E5E7EB; border-radius: 10px; padding: 1.1rem; background: #FFFFFF;">
                <div style="font-size: 0.76rem; font-weight: 600; text-transform: uppercase; color: #3B82F6; letter-spacing: 0.05em;">Step 2 • Practical Project</div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #111827; margin: 4px 0 8px 0;">{top_missing_focus[1] if len(top_missing_focus) > 1 else 'Caching & Distributed Systems'}</div>
                <div style="font-size: 0.84rem; color: #6B7280; line-height: 1.5;">
                    Implement an end-to-end full-stack or backend portfolio project integrating these tools with automated unit testing.
                </div>
                <div style="margin-top: 10px;">
                    <span class="pill-tag pill-blue">Est: 2-3 Weeks</span>
                    <span class="pill-tag pill-neutral">Portfolio Piece</span>
                </div>
            </div>

            <div style="border: 1px solid #E5E7EB; border-radius: 10px; padding: 1.1rem; background: #FFFFFF;">
                <div style="font-size: 0.76rem; font-weight: 600; text-transform: uppercase; color: #10B981; letter-spacing: 0.05em;">Step 3 • Placement Readiness</div>
                <div style="font-size: 1.05rem; font-weight: 600; color: #111827; margin: 4px 0 8px 0;">Interview Simulation</div>
                <div style="font-size: 0.84rem; color: #6B7280; line-height: 1.5;">
                    Rehearse trade-off explanations, STAR behavioral stories, system design questions, and update resume bullets.
                </div>
                <div style="margin-top: 10px;">
                    <span class="pill-tag pill-green">Final Polish</span>
                    <span class="pill-tag pill-neutral">Mock Interviews</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
