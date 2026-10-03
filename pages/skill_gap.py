"""
skill_gap.py
Interactive Skill Gap Analyzer page.
Pinpoints missing required skills, nice-to-haves, and visualizes candidate readiness.
"""

import os
import sys
import streamlit as st
import pandas as pd

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.database import get_db_connection
from analyzer.skill_gap import analyze_skill_gap
from utils.helpers import create_gauge_chart, create_skills_comparison_chart

st.set_page_config(page_title="Skill Gap | AI Resume Analyzer", page_icon="🔍", layout="wide")

st.title("🔍 Skill Gap Analysis")
st.markdown("Perform comprehensive gap analysis to identify missing competencies needed to pass technical screening.")

if "resume_data" not in st.session_state or st.session_state["resume_data"] is None:
    st.warning("⚠️ No resume found in session. Please upload a resume first.")
else:
    resume = st.session_state["resume_data"]
    candidate_skills = resume["skills"]

    with get_db_connection() as conn:
        df_roles = pd.read_sql_query("SELECT * FROM job_roles", conn)

    role_options = df_roles["role_title"].tolist() if not df_roles.empty else []
    selected_role_title = st.selectbox("Select Target Job Role:", role_options)

    if selected_role_title:
        role_row = df_roles[df_roles["role_title"] == selected_role_title].iloc[0]
        req_skills = [s.strip() for s in str(role_row["required_skills"]).split(",") if s.strip()]
        pref_skills = [s.strip() for s in str(role_row["preferred_skills"]).split(",") if s.strip()]

        gap = analyze_skill_gap(candidate_skills, req_skills, pref_skills)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(
                create_gauge_chart(gap["match_percentage"], title="Role Preparedness"),
                use_container_width=True
            )
        with col2:
            st.plotly_chart(
                create_skills_comparison_chart(len(gap["matched_skills"]), len(gap["missing_required"])),
                use_container_width=True
            )

        st.markdown(
            f"### Readiness Status: <span style='color:{gap['readiness_color']}; font-weight:bold;'>{gap['readiness_label']}</span>",
            unsafe_allow_html=True
        )

        st.divider()

        # Detailed cards
        c_req, c_miss = st.columns(2)
        with c_req:
            st.success(f"✅ Matched Skills ({len(gap['matched_skills'])})")
            if gap["matched_skills"]:
                for s in gap["matched_skills"]:
                    st.markdown(f"- **{s}** (Verified in resume)")
            else:
                st.write("None matched.")

        with c_miss:
            st.error(f"❌ Critical Missing Skills ({len(gap['missing_required'])})")
            if gap["missing_required"]:
                for s in gap["missing_required"]:
                    st.markdown(f"- **{s}** *(High Priority Requirement)*")
            else:
                st.write("No missing required skills! You cover all baseline criteria.")

        st.divider()
        st.subheader("🌟 Additional Candidate Strengths")
        if gap["extra_skills"]:
            st.write("Skills you possess that provide a competitive edge beyond the minimum role requirements:")
            st.write(", ".join([f"`{s}`" for s in gap["extra_skills"]]))
        else:
            st.info("No additional domain skills identified.")
