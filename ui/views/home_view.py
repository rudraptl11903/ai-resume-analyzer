"""
home_view.py
Home Page for AI Resume Analyzer.
Minimal, spacious, ChatGPT-inspired hero section with primary/secondary actions,
feature cards, and integrated file upload/demo loader.
"""

import streamlit as st
from ui.components import render_top_bar, render_clean_card, render_status_alert, render_pill
from ui.demo_data import get_demo_resume
from utils.pdf_reader import extract_text_from_file
from nlp.resume_parser import parse_resume
from analyzer.resume_score import calculate_resume_score
from utils.helpers import calculate_file_hash


def render_home_page():
    candidate_name = None
    if st.session_state.get("resume_data"):
        candidate_name = st.session_state["resume_data"].get("candidate_name")

    render_top_bar("Home", candidate_name=candidate_name)

    # Hero Section
    st.markdown(
        """
        <div class="hero-wrapper">
            <div class="hero-title">AI Resume Analyzer</div>
            <div class="hero-subtitle">Analyze. Match. Improve. Grow.</div>
            <div class="hero-description">
                Analyze your resume, compare it with job descriptions, identify skill gaps,
                check ATS compatibility, and receive personalized career recommendations.
            </div>
            <div class="hero-badge-row">
                <span class="hero-badge">⚡ Zero Cloud Dependencies</span>
                <span class="hero-badge">🧠 Scikit-Learn TF-IDF</span>
                <span class="hero-badge">📑 PyMuPDF Extraction</span>
                <span class="hero-badge">💾 Local SQLite</span>
                <span class="hero-badge">🔒 100% Private & Local</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Primary & Secondary Action Buttons
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    with col_btn1:
        upload_clicked = st.button("📤 Upload Resume", type="primary", use_container_width=True)
    with col_btn2:
        demo_clicked = st.button("✨ Try Demo", type="secondary", use_container_width=True)

    if demo_clicked:
        demo = get_demo_resume()
        st.session_state["resume_data"] = demo["resume_data"]
        st.session_state["resume_score"] = demo["resume_score"]
        st.session_state["current_file_hash"] = demo["file_hash"]
        render_status_alert("Demo profile for **Alex Chen (Software Engineer)** successfully loaded!", alert_type="green", title="Demo Loaded")
        st.rerun()

    # Expandable or direct uploader area
    show_uploader = upload_clicked or ("show_uploader" in st.session_state and st.session_state["show_uploader"])
    if upload_clicked:
        st.session_state["show_uploader"] = True

    # PDF-Only File Uploader
    uploaded_file = st.file_uploader(
        "Upload PDF Resume:",
        type=["pdf"],
        key="home_resume_uploader",
        help="Upload a PDF resume document (PDF only). Text is extracted locally using PyMuPDF."
    )

    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_hash = calculate_file_hash(file_bytes)

        if st.session_state.get("current_file_hash") != file_hash:
            with st.spinner("Extracting and cleaning text using PyMuPDF..."):
                extracted = extract_text_from_file(uploaded_file)
                if not extracted["success"]:
                    err_type = extracted.get("error_type", "extraction_failure")
                    if err_type == "empty":
                        render_status_alert(
                            f"**Empty PDF Document:** {extracted['error']}",
                            alert_type="orange",
                            title="Blank PDF Detected"
                        )
                    elif err_type == "scanned":
                        render_status_alert(
                            f"**Scanned / Image-Only PDF:** {extracted['error']}",
                            alert_type="orange",
                            title="No Selectable Text Found"
                        )
                    elif err_type == "corrupted":
                        render_status_alert(
                            f"**Corrupted PDF:** {extracted['error']}",
                            alert_type="red",
                            title="File Error"
                        )
                    else:
                        render_status_alert(
                            f"**Extraction Failure:** {extracted['error']}",
                            alert_type="red",
                            title="Error"
                        )
                else:
                    # Cleaned extracted text is processed through NLP parser
                    raw_text = extracted["text"]
                    parsed = parse_resume(raw_text, filename=uploaded_file.name)
                    parsed["file_size_formatted"] = extracted["file_size_formatted"]
                    parsed["page_count"] = extracted["page_count"]
                    score_data = calculate_resume_score(parsed)

                    # Store temporarily in session state for cross-module analysis
                    st.session_state["resume_data"] = parsed
                    st.session_state["resume_score"] = score_data
                    st.session_state["current_file_hash"] = file_hash
                    st.session_state["extracted_metadata"] = extracted
                    render_status_alert(
                        f"Resume successfully extracted for **{parsed['candidate_name']}** ({extracted['file_size_formatted']}, {extracted['page_count']} page{'s' if extracted['page_count'] > 1 else ''})!",
                        alert_type="green",
                        title="PDF Processed"
                    )
                    st.rerun()

    # Active Profile Snapshot & Text Preview if loaded
    if st.session_state.get("resume_data"):
        data = st.session_state["resume_data"]
        score = st.session_state["resume_score"]
        file_size_str = data.get("file_size_formatted", "PDF Document")

        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 1.2rem 1.5rem; margin-top: 1rem; margin-bottom: 1rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="width: 44px; height: 44px; border-radius: 10px; background: #111827; color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem;">
                        {data['candidate_name'][:2].upper()}
                    </div>
                    <div>
                        <div style="font-weight: 600; font-size: 1.05rem; color: #111827;">{data['candidate_name']}</div>
                        <div style="font-size: 0.84rem; color: #6B7280;">
                            {data['email']} • {data['phone']} • {data['filename']} ({file_size_str})
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 12px; align-items: center;">
                    <span class="pill-tag pill-green">Score: {score['overall_score']}/100</span>
                    <span class="pill-tag pill-blue">ATS: {score['ats_score']}%</span>
                    <span class="pill-tag pill-neutral">{len(data['skills'])} Skills</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("📄 Preview Extracted Resume Text", expanded=False):
            st.caption(f"Showing cleaned extracted text ({data['word_count']} words, {len(data.get('raw_text', ''))} characters) from {data['filename']}:")
            st.text_area(
                "Cleaned Resume Text Preview:",
                value=data.get("raw_text", ""),
                height=240,
                disabled=True,
                key="home_text_preview_box"
            )

    st.markdown("<h3 style='font-size: 1.25rem; font-weight: 600; margin-top: 2rem; margin-bottom: 1.25rem;'>Core Intelligence Modules</h3>", unsafe_allow_html=True)

    # Four Feature Cards
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            render_clean_card(
                title="Resume Analysis",
                description="Deep structural parsing, contact extraction, section validation, and categorized technical skill discovery.",
                icon="📄",
                extra_badge="Extraction"
            ),
            unsafe_allow_html=True
        )
        if st.button("Open Analysis", key="nav_home_analysis", use_container_width=True):
            st.session_state["nav_selection"] = "Resume Analysis"
            st.rerun()

    with c2:
        st.markdown(
            render_clean_card(
                title="Job Matching",
                description="Scikit-Learn TF-IDF cosine similarity comparison against benchmark roles or custom pasted job postings.",
                icon="🎯",
                extra_badge="Cosine ML"
            ),
            unsafe_allow_html=True
        )
        if st.button("Open Matcher", key="nav_home_matcher", use_container_width=True):
            st.session_state["nav_selection"] = "Job Matcher"
            st.rerun()

    with c3:
        st.markdown(
            render_clean_card(
                title="Skill Gap Analysis",
                description="Pinpoint critical missing technical skills, nice-to-haves, and structured learning roadmaps with resources.",
                icon="🔍",
                extra_badge="Gap Insights"
            ),
            unsafe_allow_html=True
        )
        if st.button("Open Skill Gap", key="nav_home_skill_gap", use_container_width=True):
            st.session_state["nav_selection"] = "Skill Gap"
            st.rerun()

    with c4:
        st.markdown(
            render_clean_card(
                title="ATS Checker",
                description="Applicant Tracking System compliance audit checking action verbs, quantification, headers, and length.",
                icon="✅",
                extra_badge="Compliance"
            ),
            unsafe_allow_html=True
        )
        if st.button("Open ATS Checker", key="nav_home_ats", use_container_width=True):
            st.session_state["nav_selection"] = "ATS Checker"
            st.rerun()
