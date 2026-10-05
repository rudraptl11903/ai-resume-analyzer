"""
settings_view.py
System settings, NLP & ML engine diagnostics, database maintenance,
and candidate profile session controls.
"""

import os
import streamlit as st
import pandas as pd
from ui.components import render_top_bar, render_pill, render_status_alert
from database.database import init_db, load_default_roles_if_empty, get_db_connection, DB_PATH


def render_settings_page():
    candidate_name = None
    if st.session_state.get("resume_data"):
        candidate_name = st.session_state["resume_data"].get("candidate_name")

    render_top_bar("Settings", candidate_name=candidate_name)

    st.markdown(
        """
        <div class="clean-card">
            <div class="card-heading">⚙️ Application Preferences & System Configuration</div>
            <div class="card-subtext">Manage evaluation thresholds, database state, and examine engine diagnostics.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(
            """
            <div class="clean-card">
                <div class="card-heading">🎯 Scoring Preferences</div>
                <div class="card-subtext">Customize algorithmic scoring weights for placement evaluations.</div>
            """,
            unsafe_allow_html=True
        )
        ats_mode = st.selectbox(
            "ATS Strictness Level:",
            ["Standard (Greenhouse / Lever baseline)", "Strict (Workday Enterprise)", "Lenient (Early-stage startup)"]
        )
        min_skills = st.slider("Target Skill Count for Junior Roles:", 5, 25, 12)
        st.caption("Adjusting target count modifies the baseline skill breadth weighting in Overall Score.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown(
            """
            <div class="clean-card">
                <div class="card-heading">💾 Local Database Administration</div>
                <div class="card-subtext">Direct interface to SQLite database storage (`database/resume_analyzer.db`).</div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(f"**Database Location:** `{DB_PATH}`")
        if os.path.exists(DB_PATH):
            size_kb = round(os.path.getsize(DB_PATH) / 1024, 1)
            st.markdown(f"**File Size:** `{size_kb} KB`")

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("🔄 Re-seed Job Roles", use_container_width=True):
                init_db()
                load_default_roles_if_empty()
                st.success("Default benchmark roles verified in database.")
        with col_b2:
            if st.button("🧹 Clear Session Resume", use_container_width=True):
                st.session_state["resume_data"] = None
                st.session_state["resume_score"] = None
                st.session_state["current_file_hash"] = None
                st.session_state.pop("last_match_results", None)
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # Diagnostics Card
    st.markdown(
        """
        <div class="clean-card">
            <div class="card-heading">🔬 System & NLP Diagnostics</div>
            <div class="card-subtext">Verification of runtime dependencies, ML vectorizers, and document parsers.</div>
            <div style="margin-top: 1rem; display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 0.88rem;">
                <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px 14px;">
                    <strong>Document Extractor:</strong> PyMuPDF (Fitz)
                    <div style="color: #065F46; font-size: 0.82rem; margin-top: 2px;">🟢 Ready (PDF, DOCX, TXT support)</div>
                </div>
                <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px 14px;">
                    <strong>ML Vectorizer:</strong> Scikit-Learn TF-IDF
                    <div style="color: #065F46; font-size: 0.82rem; margin-top: 2px;">🟢 Ready (Cosine Similarity engine)</div>
                </div>
                <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px 14px;">
                    <strong>NLP Engine:</strong> spaCy & NLTK Regex Heuristics
                    <div style="color: #065F46; font-size: 0.82rem; margin-top: 2px;">🟢 Ready (Entities, action verbs, metrics)</div>
                </div>
                <div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px 14px;">
                    <strong>Database:</strong> Local SQLite3
                    <div style="color: #065F46; font-size: 0.82rem; margin-top: 2px;">🟢 Connected (Persistent local ACID)</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
