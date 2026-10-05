"""
app.py
Main entry point for AI Resume Analyzer.
ChatGPT-inspired minimal, clean, black-and-white professional interface.
Built with Python, Streamlit, PyMuPDF, Scikit-Learn (TF-IDF), spaCy/NLTK, and SQLite.
"""

import os
import sys
import streamlit as st

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.database import init_db, load_default_roles_if_empty
from ui.styles import CUSTOM_CSS
from ui.demo_data import get_demo_resume
from ui.views.home_view import render_home_page
from ui.views.dashboard_view import render_dashboard_page
from ui.views.resume_analysis_view import render_resume_analysis_page
from ui.views.job_matcher_view import render_job_matcher_page
from ui.views.skill_gap_view import render_skill_gap_page
from ui.views.ats_checker_view import render_ats_checker_page
from ui.views.recommendations_view import render_recommendations_page
from ui.views.history_view import render_history_page
from ui.views.settings_view import render_settings_page

# Page Configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Minimal Black-and-White Design System
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def initialize_session():
    """Initializes local SQLite database and session state."""
    init_db()
    load_default_roles_if_empty()

    if "resume_data" not in st.session_state:
        # Default initialize with rich demo resume for immediate wow experience
        demo = get_demo_resume()
        st.session_state["resume_data"] = demo["resume_data"]
        st.session_state["resume_score"] = demo["resume_score"]
        st.session_state["current_file_hash"] = demo["file_hash"]

    if "nav_selection" not in st.session_state:
        st.session_state["nav_selection"] = "Home"


def main():
    initialize_session()

    # Define Navigation Items
    nav_icons = {
        "Home": "🏠",
        "Dashboard": "📊",
        "Resume Analysis": "📄",
        "Job Matcher": "🎯",
        "Skill Gap": "🔍",
        "ATS Checker": "✅",
        "Recommendations": "💡",
        "History": "🕒",
        "Settings": "⚙️",
    }
    nav_options = list(nav_icons.keys())

    # Build Left Sidebar (ChatGPT Deep Black Aesthetic)
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-logo-container">
                <div class="sidebar-logo-icon">📄</div>
                <div>
                    <div class="sidebar-logo-text">AI Resume Analyzer</div>
                    <div class="sidebar-logo-sub">Pro Platform</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="sidebar-nav-title">Navigation</div>', unsafe_allow_html=True)

        current_nav = st.session_state.get("nav_selection", "Home")
        if current_nav not in nav_options:
            current_nav = "Home"

        selected_page = st.radio(
            label="Navigation Menu",
            options=nav_options,
            format_func=lambda x: f"{nav_icons[x]}  {x}",
            index=nav_options.index(current_nav),
            label_visibility="collapsed",
            key="sidebar_nav_radio"
        )

        # Synchronize radio selection with session state
        if selected_page != st.session_state.get("nav_selection"):
            st.session_state["nav_selection"] = selected_page
            st.rerun()

        # Sidebar Footer: Active Profile
        resume = st.session_state.get("resume_data")
        candidate_name = resume["candidate_name"] if resume else "Guest / No File"
        initials = "".join([part[0] for part in candidate_name.split() if part])[:2].upper() or "RP"

        st.markdown(
            f"""
            <div class="sidebar-footer-card">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="sidebar-avatar">{initials}</div>
                    <div style="overflow: hidden;">
                        <div style="font-weight: 600; font-size: 0.85rem; color: #FFFFFF; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">
                            {candidate_name}
                        </div>
                        <div style="font-size: 0.72rem; color: #10B981; font-weight: 500;">
                            ● Active Profile
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Route to Selected Page View
    active_view = st.session_state.get("nav_selection", "Home")

    if active_view == "Home":
        render_home_page()
    elif active_view == "Dashboard":
        render_dashboard_page()
    elif active_view == "Resume Analysis":
        render_resume_analysis_page()
    elif active_view == "Job Matcher":
        render_job_matcher_page()
    elif active_view == "Skill Gap":
        render_skill_gap_page()
    elif active_view == "ATS Checker":
        render_ats_checker_page()
    elif active_view == "Recommendations":
        render_recommendations_page()
    elif active_view == "History":
        render_history_page()
    elif active_view == "Settings":
        render_settings_page()
    else:
        render_home_page()


if __name__ == "__main__":
    main()
