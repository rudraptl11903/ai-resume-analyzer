"""
skill_gap.py
Identifies skill discrepancies between a candidate's resume and a target job role.
Computes matched skills, missing essential skills, and prioritized learning suggestions.
"""

from typing import List, Dict, Any, Set


def analyze_skill_gap(
    candidate_skills: List[str],
    required_skills: List[str],
    preferred_skills: List[str] = None
) -> Dict[str, Any]:
    """
    Compares candidate skills against role specifications.
    Returns:
    - matched_skills: Skills possessed by candidate
    - missing_required: Crucial missing skills
    - missing_preferred: Nice-to-have missing skills
    - match_percentage: Weighted readiness score
    - readiness_label: Human-readable evaluation
    """
    if preferred_skills is None:
        preferred_skills = []

    # Case-insensitive normalization mapping
    cand_map = {s.lower(): s for s in candidate_skills}
    cand_set = set(cand_map.keys())

    req_map = {s.lower(): s for s in required_skills}
    pref_map = {s.lower(): s for s in preferred_skills}

    matched_req = []
    missing_req = []
    for r_lower, r_orig in req_map.items():
        if r_lower in cand_set:
            matched_req.append(cand_map[r_lower])
        else:
            missing_req.append(r_orig)

    matched_pref = []
    missing_pref = []
    for p_lower, p_orig in pref_map.items():
        if p_lower in cand_set:
            matched_pref.append(cand_map[p_lower])
        else:
            missing_pref.append(p_orig)

    # Additional skills candidate has that weren't explicitly listed in target
    extra_skills = [
        cand_map[c_lower] for c_lower in cand_set
        if c_lower not in req_map and c_lower not in pref_map
    ]

    total_req_count = len(required_skills)
    total_pref_count = len(preferred_skills)

    # Calculate match percentage
    if total_req_count > 0:
        req_score = (len(matched_req) / total_req_count) * 80.0
    else:
        req_score = 80.0

    if total_pref_count > 0:
        pref_score = (len(matched_pref) / total_pref_count) * 20.0
    else:
        pref_score = 20.0

    match_percentage = round(min(req_score + pref_score, 100.0), 1)

    # Readiness evaluation label
    if match_percentage >= 85:
        readiness = "Strong Fit - Ready to Apply"
        readiness_color = "#10B981"  # Emerald green
    elif match_percentage >= 65:
        readiness = "Moderate Fit - Minor Skill Gaps"
        readiness_color = "#F59E0B"  # Amber
    elif match_percentage >= 40:
        readiness = "Developing Fit - Key Gaps Present"
        readiness_color = "#F97316"  # Orange
    else:
        readiness = "Low Fit - Significant Upskilling Required"
        readiness_color = "#EF4444"  # Red

    return {
        "match_percentage": match_percentage,
        "readiness_label": readiness,
        "readiness_color": readiness_color,
        "matched_skills": sorted(list(set(matched_req + matched_pref))),
        "matched_required": sorted(matched_req),
        "matched_preferred": sorted(matched_pref),
        "missing_required": sorted(missing_req),
        "missing_preferred": sorted(missing_pref),
        "extra_skills": sorted(extra_skills),
        "total_required": total_req_count,
        "total_preferred": total_pref_count,
    }
