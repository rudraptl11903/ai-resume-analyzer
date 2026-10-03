"""
NLP package for AI Resume Analyzer & Job Matcher.
Includes text cleaning, skill extraction, resume parsing, and job description analysis.
"""

from .text_cleaner import clean_text, tokenize_words, remove_stopwords, extract_sentences
from .skill_extractor import (
    extract_skills,
    extract_skills_with_categories,
    SkillExtractor,
    get_skill_extractor,
)
from .job_analyzer import parse_job_description
from .resume_parser import (
    parse_resume,
    extract_email,
    extract_phone,
    extract_candidate_name,
    identify_sections,
)

__all__ = [
    "clean_text",
    "tokenize_words",
    "remove_stopwords",
    "extract_sentences",
    "extract_skills",
    "extract_skills_with_categories",
    "SkillExtractor",
    "get_skill_extractor",
    "parse_job_description",
    "parse_resume",
    "extract_email",
    "extract_phone",
    "extract_candidate_name",
    "identify_sections",
]
