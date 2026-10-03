"""
ats_checker.py
Applicant Tracking System (ATS) compliance evaluation:
- Section completeness & headings
- Contact information detection
- Action verb strength
- Quantification & measurable metrics
- Word count & formatting health
"""

import re
from typing import Dict, Any, List

ACTION_VERBS = {
    "accelerated", "accomplished", "achieved", "acquired", "adapted", "administered",
    "analyzed", "architected", "automated", "built", "calculated", "collaborated",
    "compiled", "composed", "configured", "constructed", "created", "debugged",
    "delivered", "deployed", "designed", "developed", "devised", "diagnosed",
    "engineered", "established", "evaluated", "executed", "expanded", "expedited",
    "formulated", "generated", "implemented", "improved", "increased", "initiated",
    "installed", "integrated", "invented", "investigated", "launched", "led",
    "maintained", "managed", "maximized", "migrated", "minimized", "modeled",
    "modernized", "monitored", "negotiated", "optimized", "orchestrated", "organized",
    "overhauled", "pioneered", "planned", "programmed", "published", "redesigned",
    "reduced", "refactored", "resolved", "restructured", "revamped", "saved",
    "scaled", "scheduled", "secured", "simplified", "spearheaded", "standardized",
    "streamlined", "strengthened", "supervised", "tested", "trained", "transformed",
    "troubleshot", "unified", "upgraded", "validated", "verified"
}


def check_ats_compliance(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates resume against standard ATS parsing requirements.
    Returns composite score (0-100), detailed checklist items, and improvement tips.
    """
    raw_text = resume_data.get("raw_text", "")
    word_count = resume_data.get("word_count", 0)
    sections = resume_data.get("sections", {})
    email = resume_data.get("email")
    phone = resume_data.get("phone")
    links = resume_data.get("links", {})

    checks: List[Dict[str, Any]] = []
    score_points = 0
    max_points = 100

    # 1. Contact Information (20 points)
    has_email = email and email != "Not detected"
    has_phone = phone and phone != "Not detected"
    has_profile_links = bool(links.get("linkedin") or links.get("github"))

    contact_pts = 0
    if has_email:
        contact_pts += 10
    if has_phone:
        contact_pts += 5
    if has_profile_links:
        contact_pts += 5
    score_points += contact_pts

    checks.append({
        "category": "Contact Information",
        "title": "Contact Details Detected",
        "passed": has_email and has_phone,
        "points": contact_pts,
        "max_points": 20,
        "detail": f"Email: {'Found' if has_email else 'Missing'}, Phone: {'Found' if has_phone else 'Missing'}, Links: {'Found' if has_profile_links else 'None'}"
    })

    # 2. Key Sections Present (25 points)
    # Required: Education, Experience, Projects, Skills (5 pts each) + Certifications/Summary (5 pts)
    section_pts = 0
    missing_sections = []
    for sec_key, sec_name, pts in [
        ("education", "Education", 7),
        ("experience", "Experience / Internships", 7),
        ("projects", "Projects", 6),
        ("skills", "Skills Section", 5),
    ]:
        if sections.get(sec_key, False):
            section_pts += pts
        else:
            missing_sections.append(sec_name)
    score_points += section_pts

    checks.append({
        "category": "Structure & Sections",
        "title": "Core ATS Sections",
        "passed": len(missing_sections) == 0,
        "points": section_pts,
        "max_points": 25,
        "detail": "All key sections found" if not missing_sections else f"Missing headers: {', '.join(missing_sections)}"
    })

    # 3. Action Verbs Usage (20 points)
    words_lower = set(re.findall(r"\b[a-z]+\b", raw_text.lower()))
    used_verbs = sorted(list(words_lower.intersection(ACTION_VERBS)))
    action_verb_count = len(used_verbs)

    if action_verb_count >= 10:
        verb_pts = 20
    elif action_verb_count >= 6:
        verb_pts = 14
    elif action_verb_count >= 3:
        verb_pts = 8
    else:
        verb_pts = 4
    score_points += verb_pts

    checks.append({
        "category": "Action Verbs",
        "title": "Impact-Driven Action Verbs",
        "passed": action_verb_count >= 6,
        "points": verb_pts,
        "max_points": 20,
        "detail": f"Found {action_verb_count} distinct strong action verbs (e.g., {', '.join(used_verbs[:5]) if used_verbs else 'None'})"
    })

    # 4. Quantification & Numbers (20 points)
    # Look for metrics, %, $, numbers with impact
    metrics_matches = re.findall(r"\b(?:\d+%(?:\.\d+)?|\$\d+(?:,\d+)*(?:\.\d+)?|\b\d{1,4}\b(?:\+)?(?:\s+(?:users|clients|requests|ms|seconds|minutes|tests|accuracy|increase|decrease|reduction|growth)))", raw_text, re.IGNORECASE)
    metrics_count = len(metrics_matches)

    if metrics_count >= 6:
        metric_pts = 20
    elif metrics_count >= 3:
        metric_pts = 14
    elif metrics_count >= 1:
        metric_pts = 8
    else:
        metric_pts = 3
    score_points += metric_pts

    checks.append({
        "category": "Quantification & Impact",
        "title": "Measurable Results & Metrics",
        "passed": metrics_count >= 3,
        "points": metric_pts,
        "max_points": 20,
        "detail": f"Found {metrics_count} quantifiable statements or numeric milestones."
    })

    # 5. Length & Word Count Health (15 points)
    # Optimal for student/junior: 350 - 900 words
    if 350 <= word_count <= 950:
        length_pts = 15
        length_msg = f"Ideal resume length ({word_count} words)"
        length_pass = True
    elif 200 <= word_count < 350:
        length_pts = 9
        length_msg = f"Slightly short ({word_count} words). Consider expanding project details."
        length_pass = False
    elif 950 < word_count <= 1400:
        length_pts = 10
        length_msg = f"Long resume ({word_count} words). Aim for a crisp 1-page format."
        length_pass = False
    else:
        length_pts = 5
        length_msg = f"Word count outside optimal range ({word_count} words)."
        length_pass = False
    score_points += length_pts

    checks.append({
        "category": "Formatting & Length",
        "title": "Length & Density Check",
        "passed": length_pass,
        "points": length_pts,
        "max_points": 15,
        "detail": length_msg
    })

    # Compile actionable suggestions
    suggestions: List[str] = []
    if not has_email:
        suggestions.append("Add a clear, professional email address at the very top.")
    if not has_phone:
        suggestions.append("Add your phone number with country code.")
    if not has_profile_links:
        suggestions.append("Include clickable links to your GitHub and LinkedIn profiles.")
    if missing_sections:
        suggestions.append(f"Add standard section headers: {', '.join(missing_sections)}.")
    if action_verb_count < 6:
        suggestions.append("Start bullet points with strong power verbs like 'Architected', 'Implemented', 'Optimized'.")
    if metrics_count < 3:
        suggestions.append("Quantify your achievements (e.g., 'Improved query latency by 35%', 'Built API handling 1,000+ requests/day').")
    if word_count < 350:
        suggestions.append("Flesh out bullet points with technologies used, problems solved, and business/system impact.")

    return {
        "ats_score": min(score_points, max_points),
        "checks": checks,
        "used_action_verbs": used_verbs,
        "metrics_found": metrics_matches[:10],
        "suggestions": suggestions,
    }
