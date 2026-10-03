"""
resume_parser.py
Parses resume text to extract candidate metadata:
- Contact information (Email, Phone, LinkedIn, GitHub)
- Candidate name heuristics & NLP named entity recognition
- Section segmentations (Education, Experience, Projects, Skills)
- Extracted skills and summary metrics
"""

import re
from typing import Dict, Any, List, Optional
from .skill_extractor import extract_skills, extract_skills_with_categories
from .text_cleaner import clean_text

# Lazy load spacy model if available
_spacy_nlp = None

def get_spacy_nlp():
    global _spacy_nlp
    if _spacy_nlp is None:
        try:
            import spacy
            _spacy_nlp = spacy.load("en_core_web_sm")
        except Exception:
            _spacy_nlp = False
    return _spacy_nlp if _spacy_nlp is not False else None


def extract_email(text: str) -> Optional[str]:
    """Extracts email address using standard regex."""
    if not text:
        return None
    match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extracts phone number with support for international and standard formats."""
    if not text:
        return None
    # Matches: +1-555-555-5555, (555) 555-5555, +91 9876543210, 555-555-5555, 9876543210
    pattern = r"(?:(?:\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}|\+?\d{10,14})"
    match = re.search(pattern, text)
    return match.group(0).strip() if match else None


def extract_links(text: str) -> Dict[str, Optional[str]]:
    """Extracts professional links such as LinkedIn and GitHub."""
    links: Dict[str, Optional[str]] = {"linkedin": None, "github": None, "portfolio": None}
    if not text:
        return links

    linkedin_match = re.search(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_\-\.%]+", text, re.IGNORECASE)
    if linkedin_match:
        links["linkedin"] = linkedin_match.group(0)

    github_match = re.search(r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_\-\.%]+", text, re.IGNORECASE)
    if github_match:
        links["github"] = github_match.group(0)

    portfolio_match = re.search(r"(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.(?:dev|io|me|tech|app)(?:/\S*)?", text, re.IGNORECASE)
    if portfolio_match:
        links["portfolio"] = portfolio_match.group(0)

    return links


def extract_candidate_name(text: str) -> str:
    """
    Infers candidate name from resume header lines:
    1. Checks the first 3 non-empty lines for typical name structures.
    2. Falls back to spaCy Named Entity Recognition (PERSON).
    """
    if not text:
        return "Candidate"

    lines = [line.strip() for line in text.split("\n") if line.strip()]
    header_lines = lines[:4]

    # Heuristic 1: Look at the very first line if it looks like a clean 2-3 word name
    for line in header_lines:
        clean_line = re.sub(r"[^a-zA-Z\s]", "", line).strip()
        words = clean_line.split()
        if 2 <= len(words) <= 4:
            # Check it's not a common section title or contact keyword
            lower = clean_line.lower()
            if not any(kw in lower for kw in ["resume", "curriculum", "vitae", "profile", "contact", "developer", "engineer", "phone", "email"]):
                return " ".join(w.capitalize() for w in words)

    # Heuristic 2: spaCy NER
    nlp = get_spacy_nlp()
    if nlp:
        try:
            doc = nlp("\n".join(header_lines))
            for ent in doc.ents:
                if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                    return ent.text.strip()
        except Exception:
            pass

    return lines[0][:30] if lines else "Candidate"


def identify_sections(text: str) -> Dict[str, bool]:
    """Identifies the presence of key ATS resume sections."""
    if not text:
        return {}

    text_lower = text.lower()
    sections = {
        "contact_info": bool(extract_email(text) or extract_phone(text)),
        "education": bool(re.search(r"\b(education|academic|degree|university|college|gpa)\b", text_lower)),
        "experience": bool(re.search(r"\b(experience|employment|work history|professional experience|internship)\b", text_lower)),
        "projects": bool(re.search(r"\b(projects|personal projects|technical projects|portfolio)\b", text_lower)),
        "skills": bool(re.search(r"\b(skills|technical skills|competencies|technologies|tools)\b", text_lower)),
        "certifications": bool(re.search(r"\b(certifications?|licenses?|credentials?)\b", text_lower)),
    }
    return sections


def parse_resume(raw_text: str, filename: str = "resume.pdf") -> Dict[str, Any]:
    """
    Master function to parse a resume document.
    Returns structured data dictionary ready for analysis and database storage.
    """
    candidate_name = extract_candidate_name(raw_text)
    email = extract_email(raw_text)
    phone = extract_phone(raw_text)
    links = extract_links(raw_text)
    sections = identify_sections(raw_text)
    skills = extract_skills(raw_text)
    skills_by_category = extract_skills_with_categories(raw_text)
    cleaned = clean_text(raw_text)
    word_count = len(cleaned.split())

    return {
        "filename": filename,
        "candidate_name": candidate_name,
        "email": email or "Not detected",
        "phone": phone or "Not detected",
        "links": links,
        "sections": sections,
        "skills": skills,
        "skills_by_category": skills_by_category,
        "word_count": word_count,
        "raw_text": raw_text,
        "cleaned_text": cleaned,
    }
