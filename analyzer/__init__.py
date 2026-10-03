"""
Analyzer package for AI Resume Analyzer & Job Matcher.
Includes scoring, similarity calculation, ATS checks, and skill gap identification.
"""

from .resume_score import calculate_resume_score
from .ats_checker import check_ats_compliance
from .similarity import (
    calculate_tfidf_similarity,
    calculate_jaccard_similarity,
    compute_comprehensive_match,
)
from .skill_gap import analyze_skill_gap

__all__ = [
    "calculate_resume_score",
    "check_ats_compliance",
    "calculate_tfidf_similarity",
    "calculate_jaccard_similarity",
    "compute_comprehensive_match",
    "analyze_skill_gap",
]
