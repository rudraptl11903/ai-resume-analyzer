"""
resume_score.py
Comprehensive multi-factor scoring engine for resumes.
Evaluates both standalone portfolio strength and role-targeted alignment.
"""

from typing import Dict, Any, List
from .ats_checker import check_ats_compliance


def calculate_resume_score(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes an objective, explainable baseline score for a student resume.
    Breakdown:
    1. ATS & Structure (30 pts)
    2. Technical Skill Breadth (30 pts)
    3. Project & Experience Depth (20 pts)
    4. Action-Oriented Impact (20 pts)
    """
    ats_results = check_ats_compliance(resume_data)
    ats_score = ats_results["ats_score"]

    skills = resume_data.get("skills", [])
    skills_count = len(skills)
    sections = resume_data.get("sections", {})
    raw_text = resume_data.get("raw_text", "")

    # 1. ATS Score Contribution (30%)
    ats_component = (ats_score / 100.0) * 30.0

    # 2. Skill Diversity & Repertoire (30%)
    # For a student resume, 8-15 strong technical skills is typical target
    if skills_count >= 12:
        skill_component = 30.0
    elif skills_count >= 8:
        skill_component = 24.0
    elif skills_count >= 5:
        skill_component = 18.0
    elif skills_count >= 2:
        skill_component = 10.0
    else:
        skill_component = 4.0

    # 3. Completeness of Core Sections (20%)
    completeness_pts = 0
    if sections.get("projects", False):
        completeness_pts += 8
    if sections.get("experience", False):
        completeness_pts += 6
    if sections.get("education", False):
        completeness_pts += 4
    if sections.get("certifications", False):
        completeness_pts += 2
    completeness_component = min(completeness_pts, 20.0)

    # 4. Impact & Quantifiable Results (20%)
    verb_count = len(ats_results.get("used_action_verbs", []))
    metric_count = len(ats_results.get("metrics_found", []))
    impact_raw = (verb_count * 1.2) + (metric_count * 2.0)
    impact_component = min(impact_raw, 20.0)

    overall_score = round(
        ats_component + skill_component + completeness_component + impact_component, 1
    )
    overall_score = min(max(overall_score, 0.0), 100.0)

    # Determine grade
    if overall_score >= 85:
        grade = "A (Exceptional)"
        grade_color = "#10B981"
    elif overall_score >= 70:
        grade = "B (Strong)"
        grade_color = "#3B82F6"
    elif overall_score >= 55:
        grade = "C (Fair - Needs Improvement)"
        grade_color = "#F59E0B"
    else:
        grade = "D (Needs Substantial Work)"
        grade_color = "#EF4444"

    return {
        "overall_score": overall_score,
        "grade": grade,
        "grade_color": grade_color,
        "ats_score": ats_score,
        "breakdown": {
            "ats_structure": round(ats_component, 1),
            "skill_breadth": round(skill_component, 1),
            "content_completeness": round(completeness_component, 1),
            "impact_metrics": round(impact_component, 1),
        },
        "ats_details": ats_results,
    }
