"""
skill_extractor.py
Rule-based & dictionary-driven skill extraction with n-gram phrase matching.
Supports categorization across Programming, Web, Data/AI, Cloud, and Soft Skills.
"""

import os
import re
import pandas as pd
from typing import List, Dict, Set, Tuple

SKILLS_CSV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "skills.csv")
)


class SkillExtractor:
    """Extracts and categorizes skills from technical text."""

    def __init__(self, skills_csv_path: str = SKILLS_CSV_PATH):
        self.skills_csv_path = skills_csv_path
        self.skills_db: Dict[str, str] = {}  # {normalized_skill_lower: original_skill_name}
        self.skill_categories: Dict[str, str] = {}  # {original_skill_name: category}
        self._load_skills()

    def _load_skills(self) -> None:
        """Loads skills from CSV file and pre-indexes them."""
        if os.path.exists(self.skills_csv_path):
            try:
                df = pd.read_csv(self.skills_csv_path)
                for _, row in df.iterrows():
                    skill = str(row["skill"]).strip()
                    category = str(row.get("category", "General")).strip()
                    if skill:
                        self.skills_db[skill.lower()] = skill
                        self.skill_categories[skill] = category
            except Exception as e:
                print(f"Warning: Could not load skills CSV: {e}")
                self._load_fallback_skills()
        else:
            self._load_fallback_skills()

    def _load_fallback_skills(self) -> None:
        """Fallback list of foundational skills if CSV is missing."""
        fallback = [
            ("Python", "Programming Languages"), ("Java", "Programming Languages"),
            ("C++", "Programming Languages"), ("JavaScript", "Programming Languages"),
            ("React", "Web Development"), ("Node.js", "Web Development"),
            ("SQL", "Databases"), ("PostgreSQL", "Databases"),
            ("Docker", "Cloud & DevOps"), ("Git", "Tools & Version Control"),
            ("Machine Learning", "Data Science & AI"), ("Pandas", "Data Science & AI")
        ]
        for skill, cat in fallback:
            self.skills_db[skill.lower()] = skill
            self.skill_categories[skill] = cat

    def extract_skills(self, text: str) -> List[str]:
        """
        Extracts recognized skills from text using boundary matching.
        Preserves special characters such as C++, C#, .NET, CI/CD.
        """
        if not text:
            return []

        text_lower = " " + text.lower() + " "
        found_skills: Set[str] = set()

        # Sort candidate skills by length descending (e.g. 'Data Science' before 'Data')
        sorted_skills = sorted(self.skills_db.keys(), key=lambda s: len(s), reverse=True)

        for skill_lower in sorted_skills:
            # Escape regex special characters except symbols common in tech
            escaped = re.escape(skill_lower)
            # Match with word boundaries or punctuation boundaries
            pattern = rf"(?<![\w\.\+#]){escaped}(?![\w\.\+#])"
            if re.search(pattern, text_lower):
                found_skills.add(self.skills_db[skill_lower])

        return sorted(list(found_skills))

    def extract_skills_with_categories(self, text: str) -> Dict[str, List[str]]:
        """
        Extracts skills and groups them by their category.
        Returns a dictionary: {Category: [Skill1, Skill2, ...]}
        """
        skills = self.extract_skills(text)
        categorized: Dict[str, List[str]] = {}

        for skill in skills:
            category = self.skill_categories.get(skill, "Other Technical Skills")
            categorized.setdefault(category, []).append(skill)

        # Sort both categories and internal lists
        return {cat: sorted(items) for cat, items in sorted(categorized.items())}


# Default singleton instance for quick usage
_default_extractor = None

def get_skill_extractor() -> SkillExtractor:
    global _default_extractor
    if _default_extractor is None:
        _default_extractor = SkillExtractor()
    return _default_extractor

def extract_skills(text: str) -> List[str]:
    """Helper function to extract skills using default extractor."""
    return get_skill_extractor().extract_skills(text)

def extract_skills_with_categories(text: str) -> Dict[str, List[str]]:
    """Helper function to extract categorized skills using default extractor."""
    return get_skill_extractor().extract_skills_with_categories(text)
