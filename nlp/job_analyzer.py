"""
job_analyzer.py
Parses and structures job postings or requirements text:
- Extracts required skills & technologies
- Estimates minimum experience years
- Identifies degree / education requirements
- Calculates key requirement terms
"""

import re
from typing import Dict, List, Any
from .skill_extractor import extract_skills, extract_skills_with_categories
from .text_cleaner import clean_text


def parse_job_description(job_text: str) -> Dict[str, Any]:
    """
    Analyzes job description text and extracts core criteria:
    - Skills required (categorized and flat list)
    - Years of experience mentioned
    - Education / degree requirements
    - Cleaned description text
    """
    if not job_text:
        return {
            "skills": [],
            "skills_by_category": {},
            "min_experience_years": 0,
            "education_requirements": [],
            "word_count": 0,
            "cleaned_text": "",
        }

    cleaned = clean_text(job_text)
    skills = extract_skills(job_text)
    skills_by_cat = extract_skills_with_categories(job_text)

    # Detect years of experience pattern: e.g. "3+ years", "2-4 years of experience"
    exp_matches = re.findall(
        r"(\d+)(?:\+|-(\d+))?\s*(?:to\s*(\d+))?\s*(?:years?|yrs?)(?:\s+of)?\s+experience",
        job_text,
        re.IGNORECASE
    )
    years_found = []
    for match in exp_matches:
        for val in match:
            if val and val.isdigit():
                years_found.append(int(val))

    min_exp = min(years_found) if years_found else 0

    # Detect education keywords
    education_cues = []
    edu_patterns = [
        (r"\b(?:bachelor'?s|b\.?s|b\.?tech|b\.?e)\b", "Bachelor's Degree"),
        (r"\b(?:master'?s|m\.?s|m\.?tech)\b", "Master's Degree"),
        (r"\b(?:ph\.?d|doctorate)\b", "Ph.D. / Doctorate"),
        (r"\bcomputer science\b", "Computer Science Field"),
        (r"\belectrical engineering\b", "Electrical Engineering Field"),
    ]
    for pattern, label in edu_patterns:
        if re.search(pattern, job_text, re.IGNORECASE):
            if label not in education_cues:
                education_cues.append(label)

    return {
        "skills": skills,
        "skills_by_category": skills_by_cat,
        "min_experience_years": min_exp,
        "education_requirements": education_cues,
        "word_count": len(cleaned.split()),
        "cleaned_text": cleaned,
    }
