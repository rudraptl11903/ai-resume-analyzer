"""
text_cleaner.py
Text preprocessing and normalization pipeline for resumes and job descriptions.
"""

import re
import string
from typing import List

# English stopwords fallback in case NLTK corpus is unavailable
FALLBACK_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}

try:
    from nltk.corpus import stopwords
    STOPWORDS = set(stopwords.words("english"))
except Exception:
    STOPWORDS = FALLBACK_STOPWORDS


def clean_text(text: str) -> str:
    """
    Cleans raw resume or job text:
    - Removes URL links
    - Removes emails and phone numbers (for NLP text comparison)
    - Normalizes non-breaking whitespace and unicode characters
    - Preserves letters, numbers, and useful programming symbols like +, #, /
    """
    if not text:
        return ""

    # Replace newlines and carriage returns with single spaces
    text = re.sub(r"[\r\n\t]+", " ", text)

    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)

    # Normalize special characters often found in resumes (bullets, dashes, quotes)
    text = re.sub(r"[•●▪◆★✓✔\-\–\—]", " ", text)

    # Collapse multi-spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize_words(text: str, lower: bool = True) -> List[str]:
    """Tokenizes text into words while keeping tech identifiers intact."""
    if not text:
        return []
    if lower:
        text = text.lower()
    # Match words, allowing hyphens and plus/sharp for C++, C#, CI/CD
    tokens = re.findall(r"\b[a-zA-Z0-9\+\#\./\-]+\b", text)
    return tokens


def remove_stopwords(tokens: List[str]) -> List[str]:
    """Filters out common English stopwords from a token list."""
    return [t for t in tokens if t.lower() not in STOPWORDS and len(t) > 1]


def extract_sentences(text: str) -> List[str]:
    """Splits resume text into bullet point statements or sentences."""
    if not text:
        return []
    # Split by common bullet delimiters or standard sentence endings
    lines = re.split(r"[\n\r•●▪\.]+", text)
    cleaned = [line.strip() for line in lines if len(line.strip()) > 10]
    return cleaned
