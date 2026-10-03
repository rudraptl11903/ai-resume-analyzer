"""
Utils package for AI Resume Analyzer & Job Matcher.
Includes document text extraction, hashing, and Plotly visualization builders.
"""

from .pdf_reader import extract_text_from_pdf, extract_text_from_file
from .helpers import (
    calculate_file_hash,
    create_gauge_chart,
    create_radar_chart,
    create_skills_comparison_chart,
    create_category_bar_chart,
)

__all__ = [
    "extract_text_from_pdf",
    "extract_text_from_file",
    "calculate_file_hash",
    "create_gauge_chart",
    "create_radar_chart",
    "create_skills_comparison_chart",
    "create_category_bar_chart",
]
