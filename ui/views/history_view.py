"""
history_view.py
History page displaying persistent SQLite evaluation logs, candidate scans,
score timelines, and export features.
"""

import streamlit as st
import pandas as pd
from ui.components import render_top_bar, render_pill, render_status_alert
from database.database import get_recent_analyses, get_analytics_summary, get_db_connection


def render_history_page():
    candidate_name = None
    if st.session_state.get("resume_data"):
        candidate_name = st.session_state["resume_data"].get("candidate_name")

    render_top_bar("History", candidate_name=candidate_name)

    analytics = get_analytics_summary()

    # Metric Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="clean-card" style="text-align: center; padding: 1.1rem;">
                <div style="font-size: 1.75rem; font-weight: 700; color: #111827;">{analytics['total_resumes']}</div>
                <div style="font-size: 0.8rem; color: #6B7280; font-weight: 500; text-transform: uppercase;">Total Resumes</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="clean-card" style="text-align: center; padding: 1.1rem;">
                <div style="font-size: 1.75rem; font-weight: 700; color: #111827;">{analytics['total_scans']}</div>
                <div style="font-size: 0.8rem; color: #6B7280; font-weight: 500; text-transform: uppercase;">Total Scans</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="clean-card" style="text-align: center; padding: 1.1rem;">
                <div style="font-size: 1.75rem; font-weight: 700; color: #10B981;">{analytics['avg_score']}%</div>
                <div style="font-size: 0.8rem; color: #6B7280; font-weight: 500; text-transform: uppercase;">Avg Score</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""
            <div class="clean-card" style="text-align: center; padding: 1.1rem;">
                <div style="font-size: 1.75rem; font-weight: 700; color: #3B82F6;">{analytics['avg_ats']}%</div>
                <div style="font-size: 0.8rem; color: #6B7280; font-weight: 500; text-transform: uppercase;">Avg ATS Rate</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    st.markdown(
        """
        <div class="clean-card">
            <div class="card-heading">🕒 Evaluation Logs & Audit Trail</div>
            <div class="card-subtext">Historical records stored locally in SQLite (`database/resume_analyzer.db`).</div>
        """,
        unsafe_allow_html=True
    )

    recent = get_recent_analyses(limit=50)
    if recent:
        df = pd.DataFrame(recent)
        display_cols = ["id", "candidate_name", "filename", "target_role", "overall_score", "ats_score", "match_percentage", "skills_count", "analyzed_at"]
        available_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available_cols], use_container_width=True)

        col_act1, col_act2 = st.columns([1, 4])
        with col_act1:
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export CSV",
                data=csv_data,
                file_name="resume_analysis_history.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("No evaluations recorded yet. Run a Job Matcher scan or save a profile in Resume Analysis to generate history.")

    st.markdown("</div>", unsafe_allow_html=True)
