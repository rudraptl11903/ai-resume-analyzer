"""
resume_analysis_view.py
Detailed Resume Breakdown & Scoring view.
Shows uploaded document, file information, overall resume score, personal information,
categorized skills, education, experience, projects, and certifications.
"""

import streamlit as st
from ui.components import render_top_bar, render_circular_progress, render_pill, render_status_alert
from ui.demo_data import get_demo_resume
from utils.helpers import create_radar_chart, calculate_file_hash
from utils.pdf_reader import extract_text_from_file
from nlp.resume_parser import parse_resume
from analyzer.resume_score import calculate_resume_score
from database.database import save_resume, save_analysis


def render_resume_analysis_page():
    candidate_name = None
    if st.session_state.get("resume_data"):
        candidate_name = st.session_state["resume_data"].get("candidate_name")

    render_top_bar("Resume Analysis", candidate_name=candidate_name)

    # PDF-Only Document upload bar
    uploaded_file = st.file_uploader(
        "Upload or Replace PDF Resume:",
        type=["pdf"],
        key="analysis_page_uploader",
        help="Upload a PDF resume document (PDF only). Extracted locally via PyMuPDF."
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
                    raw_text = extracted["text"]
                    parsed = parse_resume(raw_text, filename=uploaded_file.name)
                    parsed["file_size_formatted"] = extracted["file_size_formatted"]
                    parsed["page_count"] = extracted["page_count"]
                    score_data = calculate_resume_score(parsed)

                    st.session_state["resume_data"] = parsed
                    st.session_state["resume_score"] = score_data
                    st.session_state["current_file_hash"] = file_hash
                    st.session_state["extracted_metadata"] = extracted
                    render_status_alert(
                        f"Document successfully parsed and scored ({extracted['file_size_formatted']}, {extracted['page_count']} pages)!",
                        alert_type="green"
                    )
                    st.rerun()

    if not st.session_state.get("resume_data"):
        render_status_alert(
            "Please upload a PDF resume or load our demonstration profile to inspect deep candidate analysis.",
            alert_type="blue",
            title="Awaiting Document"
        )
        if st.button("✨ Load Demo Resume", type="primary"):
            demo = get_demo_resume()
            st.session_state["resume_data"] = demo["resume_data"]
            st.session_state["resume_score"] = demo["resume_score"]
            st.session_state["current_file_hash"] = demo["file_hash"]
            st.rerun()
        return

    resume = st.session_state["resume_data"]
    score = st.session_state["resume_score"]

    # =========================================================================
    # ROW 1: FILE INFORMATION & OVERALL RESUME SCORE
    # =========================================================================
    r1_col1, r1_col2 = st.columns([1, 2])

    with r1_col1:
        st.markdown(
            render_circular_progress(
                score=score["overall_score"],
                label="Overall Resume Score",
                sublabel=f"Quality Grade: {score['grade']}",
                color_type="green" if score["overall_score"] >= 80 else "blue",
                size=120,
                suffix="/100"
            ),
            unsafe_allow_html=True
        )

    with r1_col2:
        file_hash = st.session_state.get("current_file_hash", "local_file_hash")
        short_hash = f"{file_hash[:12]}..." if len(file_hash) > 12 else file_hash
        file_size_str = resume.get("file_size_formatted", "248.5 KB")
        page_count_num = resume.get("page_count", 1)
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">📄 Uploaded PDF Information</div>
                <div style="margin-top: 0.75rem; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.86rem;">
                    <div><strong>Filename:</strong> <span style="color: #4B5563;">{resume['filename']}</span></div>
                    <div><strong>File Size:</strong> <span style="color: #4B5563; font-weight: 500;">{file_size_str}</span></div>
                    <div><strong>Page Count:</strong> <span style="color: #4B5563;">{page_count_num} page{'s' if page_count_num > 1 else ''}</span></div>
                    <div><strong>Word Count:</strong> <span style="color: #4B5563;">{resume['word_count']} words</span></div>
                    <div><strong>Document Hash:</strong> <span style="font-family: monospace; font-size: 0.78rem; color: #4B5563;">{short_hash}</span></div>
                    <div><strong>Engine:</strong> <span style="color: #4B5563;">PyMuPDF + spaCy NLP</span></div>
                </div>
                <div style="margin-top: 1rem;">
                    <span class="pill-tag pill-green">ATS Compliance: {score['ats_score']}%</span>
                    <span class="pill-tag pill-blue">Skills Extracted: {len(resume['skills'])}</span>
                    <span class="pill-tag pill-neutral">Format: PDF Verified</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # =========================================================================
    # ROW 2: PERSONAL INFORMATION & DIMENSION BREAKDOWN
    # =========================================================================
    r2_col1, r2_col2 = st.columns([1, 1])

    with r2_col1:
        links = resume.get("links", {})
        link_items = []
        if links.get("linkedin"):
            link_items.append(f'<a href="{links["linkedin"]}" target="_blank" style="color: #111827; font-weight: 500;">LinkedIn ↗</a>')
        if links.get("github"):
            link_items.append(f'<a href="{links["github"]}" target="_blank" style="color: #111827; font-weight: 500;">GitHub ↗</a>')
        if links.get("portfolio"):
            link_items.append(f'<a href="{links["portfolio"]}" target="_blank" style="color: #111827; font-weight: 500;">Portfolio ↗</a>')
        links_html = " • ".join(link_items) if link_items else '<span style="color: #9CA3AF;">None detected</span>'

        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">👤 Personal Information</div>
                <div style="margin-top: 0.75rem; font-size: 0.88rem; line-height: 1.8;">
                    <div><strong>Full Name:</strong> {resume['candidate_name']}</div>
                    <div><strong>Email:</strong> <span style="color: #111827; font-family: monospace;">{resume['email']}</span></div>
                    <div><strong>Phone:</strong> {resume['phone']}</div>
                    <div><strong>Web & Social Profiles:</strong> {links_html}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with r2_col2:
        breakdown = score.get("breakdown", {})
        categories = ["ATS & Structure", "Skill Breadth", "Section Health", "Impact & Metrics"]
        values = [
            (breakdown.get("ats_structure", 25) / 30.0) * 100,
            (breakdown.get("skill_breadth", 25) / 30.0) * 100,
            (breakdown.get("content_completeness", 16) / 20.0) * 100,
            (breakdown.get("impact_metrics", 16) / 20.0) * 100,
        ]
        radar_fig = create_radar_chart(categories, values, title="Dimension Assessment")
        st.plotly_chart(radar_fig, use_container_width=True)

    st.write("")

    # =========================================================================
    # ROW 3: CATEGORIZED SKILLS
    # =========================================================================
    st.markdown(
        f"""
        <div class="clean-card">
            <div class="card-heading">🛠️ Extracted Technical Skills ({len(resume['skills'])} Total)</div>
            <div class="card-subtext">Grouped by engineering sub-disciplines according to industry taxonomy.</div>
        """,
        unsafe_allow_html=True
    )
    cat_skills = resume.get("skills_by_category", {})
    if cat_skills:
        cols = st.columns(len(cat_skills)) if len(cat_skills) <= 4 else st.columns(3)
        col_idx = 0
        for cat_name, skill_list in cat_skills.items():
            with cols[col_idx % len(cols)]:
                st.markdown(f"**{cat_name}** ({len(skill_list)})")
                pills = "".join([render_pill(s, "neutral") for s in skill_list])
                st.markdown(pills, unsafe_allow_html=True)
                st.write("")
            col_idx += 1
    else:
        pills = "".join([render_pill(s, "neutral") for s in resume.get("skills", [])])
        st.markdown(pills, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    # =========================================================================
    # ROW 4: EDUCATION, EXPERIENCE, PROJECTS, CERTIFICATIONS
    # =========================================================================
    sec_cont = resume.get("section_contents", {})

    st.markdown("<h4 style='font-size: 1.15rem; font-weight: 600; margin-top: 1rem;'>Resume Sections Breakdown</h4>", unsafe_allow_html=True)
    tab_exp, tab_proj, tab_edu, tab_cert, tab_raw = st.tabs([
        "💼 Experience", "🚀 Projects", "🎓 Education", "📜 Certifications", "📑 Raw Document Text"
    ])

    with tab_exp:
        exp_text = sec_cont.get("experience", "")
        if exp_text:
            st.markdown(f"```text\n{exp_text}\n```")
        else:
            st.info("No dedicated Experience section header detected. Information inferred from content.")

    with tab_proj:
        proj_text = sec_cont.get("projects", "")
        if proj_text:
            st.markdown(f"```text\n{proj_text}\n```")
        else:
            st.info("No dedicated Projects section header detected.")

    with tab_edu:
        edu_text = sec_cont.get("education", "")
        if edu_text:
            st.markdown(f"```text\n{edu_text}\n```")
        else:
            st.info("No dedicated Education section header detected.")

    with tab_cert:
        cert_text = sec_cont.get("certifications", "")
        if cert_text:
            st.markdown(f"```text\n{cert_text}\n```")
        else:
            st.info("No formal Certifications section detected.")

    with tab_raw:
        st.text_area("Extracted Plain Text from Document:", value=resume["raw_text"], height=320, disabled=True)

    # Save Profile Action
    st.write("")
    if st.button("💾 Save Candidate Profile to Local SQLite", type="primary"):
        resume_id = save_resume(
            filename=resume["filename"],
            candidate_name=resume["candidate_name"],
            email=resume["email"],
            phone=resume["phone"],
            raw_text=resume["raw_text"],
            page_count=1,
            file_hash=st.session_state.get("current_file_hash", "")
        )
        save_analysis(
            resume_id=resume_id,
            target_role="General Evaluation",
            overall_score=score["overall_score"],
            ats_score=score["ats_score"],
            match_percentage=score["overall_score"],
            skills_count=len(resume["skills"]),
            matched_skills=",".join(resume["skills"]),
            missing_skills=""
        )
        render_status_alert(f"Profile saved to SQLite database with Record #{resume_id}!", alert_type="green")
