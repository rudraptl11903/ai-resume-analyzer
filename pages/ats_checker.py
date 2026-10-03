"""
ats_checker.py
Applicant Tracking System (ATS) Compliance Audit Page.
Evaluates machine-readability, formatting, section headers, power verbs, and quantification.
"""

import os
import sys
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from analyzer.ats_checker import check_ats_compliance
from utils.helpers import create_gauge_chart

st.set_page_config(page_title="ATS Checker | AI Resume Analyzer", page_icon="✅", layout="wide")

st.title("✅ ATS Compliance & Readability Checker")
st.markdown("Ensure your resume successfully passes automated enterprise Applicant Tracking Systems (Workday, Greenhouse, Lever).")

if "resume_data" not in st.session_state or st.session_state["resume_data"] is None:
    st.warning("⚠️ No resume found in session. Please upload a resume first.")
else:
    resume = st.session_state["resume_data"]
    audit = check_ats_compliance(resume)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(
            create_gauge_chart(audit["ats_score"], title="ATS Readiness Score"),
            use_container_width=True
        )
        if audit["ats_score"] >= 80:
            st.success("🟢 Highly ATS-Friendly! Minimal formatting risk.")
        elif audit["ats_score"] >= 60:
            st.warning("🟡 Moderate ATS Compliance. Some adjustments advised.")
        else:
            st.error("🔴 High Risk of ATS rejection. Follow recommended fixes.")

    with col2:
        st.subheader("📋 Comprehensive ATS Audit Checklist")
        for check in audit["checks"]:
            status_icon = "✅" if check["passed"] else "⚠️"
            with st.expander(f"{status_icon} {check['title']} ({check['points']}/{check['max_points']} pts)", expanded=not check["passed"]):
                st.markdown(f"**Category:** {check['category']}")
                st.markdown(f"**Findings:** {check['detail']}")

    st.divider()

    col_v, col_m = st.columns(2)
    with col_v:
        st.subheader("⚡ Detected Power Action Verbs")
        verbs = audit.get("used_action_verbs", [])
        if verbs:
            st.write(", ".join([f"`{v}`" for v in verbs]))
            st.caption(f"Total {len(verbs)} strong impact verbs found.")
        else:
            st.warning("No standard power verbs detected. Start bullet points with words like 'Engineered', 'Optimized', 'Deployed'.")

    with col_m:
        st.subheader("📈 Quantified Metrics & Numbers")
        metrics = audit.get("metrics_found", [])
        if metrics:
            st.write(", ".join([f"`{m}`" for m in metrics]))
            st.caption(f"Total {len(metrics)} quantifiable indicators detected.")
        else:
            st.warning("No quantified metrics found. Include percentages, dollar savings, or latency improvements.")

    if audit.get("suggestions"):
        st.divider()
        st.subheader("🛠️ Actionable ATS Fixes")
        for idx, tip in enumerate(audit["suggestions"], 1):
            st.markdown(f"**{idx}.** {tip}")
