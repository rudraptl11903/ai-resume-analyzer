"""
dashboard.py
Analytics Dashboard for AI Resume Analyzer & Job Matcher.
Visualizes database statistics, recent resume scans, score distributions, and role demand.
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.database import (
    init_db,
    get_recent_analyses,
    get_analytics_summary,
    load_default_roles_if_empty,
    get_db_connection
)

st.set_page_config(page_title="Dashboard | AI Resume Analyzer", page_icon="📊", layout="wide")

st.title("📊 System Analytics & Recent Scans")
st.markdown("Monitor candidate evaluation history, score distributions, and top in-demand skills from local SQLite storage.")

init_db()
load_default_roles_if_empty()

analytics = get_analytics_summary()

# Key metric cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Resumes Analyzed", analytics["total_resumes"])
with c2:
    st.metric("Total Role Evaluations", analytics["total_scans"])
with c3:
    st.metric("Average Overall Score", f"{analytics['avg_score']}/100")
with c4:
    st.metric("Average ATS Score", f"{analytics['avg_ats']}%")

st.divider()

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("🕒 Recent Resume Evaluations")
    recent = get_recent_analyses(limit=10)
    if recent:
        df_recent = pd.DataFrame(recent)
        # Select and format columns for clean display
        display_cols = ["candidate_name", "filename", "target_role", "overall_score", "ats_score", "match_percentage", "analyzed_at"]
        available_cols = [c for c in display_cols if c in df_recent.columns]
        st.dataframe(df_recent[available_cols], use_container_width=True)
    else:
        st.info("No evaluations recorded yet. Upload a resume on the Home page or Resume Analysis page to begin!")

with col_right:
    st.subheader("🎯 Available Target Job Roles")
    with get_db_connection() as conn:
        df_roles = pd.read_sql_query("SELECT role_title, category, experience_level FROM job_roles", conn)
        if not df_roles.empty:
            st.dataframe(df_roles, use_container_width=True)
        else:
            st.write("No job roles registered.")

st.divider()
st.caption("SQLite local database located at `database/resume_analyzer.db` | Zero cloud API dependencies")
