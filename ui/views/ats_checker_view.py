"""
ats_checker_view.py
Applicant Tracking System (ATS) Compliance Audit Page.
Shows ATS score, structured checklist, passed checks, failed checks,
and AI-driven resume improvement suggestions.
"""

import streamlit as st
from ui.components import render_top_bar, render_circular_progress, render_pill, render_status_alert
from ui.demo_data import get_demo_resume
from analyzer.ats_checker import check_ats_compliance


def render_ats_checker_page():
    candidate_name = None
    if st.session_state.get("resume_data"):
        candidate_name = st.session_state["resume_data"].get("candidate_name")

    render_top_bar("ATS Checker", candidate_name=candidate_name)

    if not st.session_state.get("resume_data"):
        render_status_alert(
            "Please upload a resume on the Home page or load our demo profile to run the ATS compliance audit.",
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
    audit = check_ats_compliance(resume)
    ats_score = audit["ats_score"]

    # =========================================================================
    # ROW 1: ATS SCORE & READINESS TIER
    # =========================================================================
    r1_col1, r1_col2 = st.columns([1, 2])

    with r1_col1:
        st.markdown(
            render_circular_progress(
                score=ats_score,
                label="ATS Compliance Score",
                sublabel="Machine Readability",
                color_type="green" if ats_score >= 80 else ("orange" if ats_score >= 60 else "red"),
                size=120,
                suffix="%"
            ),
            unsafe_allow_html=True
        )

    with r1_col2:
        if ats_score >= 80:
            badge_html = '<span class="pill-tag pill-green">🟢 High Readability • Minimal Screening Risk</span>'
            status_desc = "Your resume structure adheres closely to automated parsing standards utilized by Workday, Greenhouse, and Lever. Standard section titles, impact verbs, and contact info are readily parsable."
        elif ats_score >= 60:
            badge_html = '<span class="pill-tag pill-orange">🟡 Moderate Compliance • Some Adjustments Needed</span>'
            status_desc = "Your resume will likely pass baseline parsers, but missing quantifiable metrics, section headers, or action verbs could reduce its overall ranking in recruiter search filters."
        else:
            badge_html = '<span class="pill-tag pill-red">🔴 High Screening Risk • Action Required</span>'
            status_desc = "Automated parsers may fail to extract your contact details, education, or key skills correctly. Review the failed checks below to ensure your resume is not discarded before a recruiter sees it."

        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">📋 Enterprise ATS Parsing Assessment</div>
                <div style="margin-top: 0.5rem;">{badge_html}</div>
                <div style="margin-top: 0.75rem; font-size: 0.88rem; color: #4B5563; line-height: 1.6;">
                    {status_desc}
                </div>
                <div style="margin-top: 1rem;">
                    <span class="pill-tag pill-neutral">{resume['word_count']} Total Words</span>
                    <span class="pill-tag pill-neutral">{len(audit.get('used_action_verbs', []))} Power Verbs</span>
                    <span class="pill-tag pill-neutral">{len(audit.get('metrics_found', []))} Quantified Metrics</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # =========================================================================
    # ROW 2: PASSED CHECKS VS FAILED CHECKS
    # =========================================================================
    checks = audit.get("checks", [])
    passed_checks = [c for c in checks if c["passed"]]
    failed_checks = [c for c in checks if not c["passed"]]

    col_pass, col_fail = st.columns(2)

    with col_pass:
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">✅ Passed Checks ({len(passed_checks)})</div>
                <div class="card-subtext">Components successfully verified for ATS compliance.</div>
                <div style="margin-top: 1rem;">
            """,
            unsafe_allow_html=True
        )
        if passed_checks:
            for chk in passed_checks:
                st.markdown(
                    f"""
                    <div style="border: 1px solid #A7F3D0; background: #ECFDF5; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 600; font-size: 0.88rem; color: #065F46;">✓ {chk['title']}</span>
                            <span class="pill-tag pill-green">+{chk['points']} pts</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #047857; margin-top: 4px;">{chk['detail']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No checks passed yet.")
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_fail:
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">⚠️ Failed / Incomplete Checks ({len(failed_checks)})</div>
                <div class="card-subtext">Areas requiring modification to maximize ATS ranking.</div>
                <div style="margin-top: 1rem;">
            """,
            unsafe_allow_html=True
        )
        if failed_checks:
            for chk in failed_checks:
                st.markdown(
                    f"""
                    <div style="border: 1px solid #FECACA; background: #FEF2F2; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 600; font-size: 0.88rem; color: #991B1B;">✕ {chk['title']}</span>
                            <span class="pill-tag pill-red">{chk['points']}/{chk['max_points']} pts</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #B91C1C; margin-top: 4px;">{chk['detail']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                """
                <div style="border: 1px solid #A7F3D0; background: #ECFDF5; border-radius: 8px; padding: 14px; text-align: center;">
                    <div style="font-weight: 600; color: #065F46;">🎉 Zero Failed Checks!</div>
                    <div style="font-size: 0.84rem; color: #047857; margin-top: 4px;">Your resume meets all baseline automated parsing criteria.</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.write("")

    # =========================================================================
    # ROW 3: AI IMPROVEMENT SUGGESTIONS
    # =========================================================================
    suggestions = audit.get("suggestions", [])
    if not suggestions:
        suggestions = [
            "Quantify remaining bullet points with exact metrics (e.g. latency reduction %, requests processed/sec, dollar savings).",
            "Maintain consistent date formatting throughout (e.g., 'May 2025 - Aug 2025') across experience and project entries.",
            "Tailor technical keywords directly from target job postings into your skills and project summaries."
        ]

    st.markdown(
        """
        <div class="clean-card">
            <div class="card-heading">💡 AI Improvement Suggestions</div>
            <div class="card-subtext">Actionable, machine-verified optimizations to boost resume score and recruiter engagement.</div>
            <div style="margin-top: 1rem;">
        """,
        unsafe_allow_html=True
    )

    for idx, tip in enumerate(suggestions, 1):
        st.markdown(
            f"""
            <div style="border: 1px solid #DDD6FE; background: #F5F3FF; border-radius: 8px; padding: 12px 16px; margin-bottom: 10px; display: flex; align-items: flex-start; gap: 12px;">
                <div style="background: #8B5CF6; color: white; border-radius: 50%; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; font-size: 0.76rem; font-weight: 700; flex-shrink: 0;">
                    {idx}
                </div>
                <div style="font-size: 0.88rem; color: #4C1D95; line-height: 1.5;">
                    {tip}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div></div>", unsafe_allow_html=True)

    st.write("")

    # =========================================================================
    # ROW 4: DETECTED POWER ACTION VERBS & QUANTIFIED METRICS
    # =========================================================================
    col_v, col_m = st.columns(2)

    with col_v:
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">⚡ Detected Impact Action Verbs ({len(audit.get('used_action_verbs', []))})</div>
                <div class="card-subtext">High-signal verbs recognized by hiring managers and ATS filters.</div>
                <div style="margin-top: 0.75rem;">
            """,
            unsafe_allow_html=True
        )
        verbs = audit.get("used_action_verbs", [])
        if verbs:
            pills = "".join([render_pill(v, "green") for v in verbs])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.warning("No power action verbs detected. Begin bullet points with words like 'Architected', 'Engineered', 'Optimized'.")
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_m:
        st.markdown(
            f"""
            <div class="clean-card">
                <div class="card-heading">📈 Quantified Metrics & Measurable Impact ({len(audit.get('metrics_found', []))})</div>
                <div class="card-subtext">Numeric proof points demonstrating business or engineering results.</div>
                <div style="margin-top: 0.75rem;">
            """,
            unsafe_allow_html=True
        )
        metrics = audit.get("metrics_found", [])
        if metrics:
            pills = "".join([render_pill(m, "blue") for m in metrics])
            st.markdown(pills, unsafe_allow_html=True)
        else:
            st.warning("No quantified metrics detected. Add exact percentages (e.g. 42%), counts (e.g. 15,000+ users), or times.")
        st.markdown("</div></div>", unsafe_allow_html=True)
