"""
similarity.py
Machine Learning similarity metrics using scikit-learn:
- TF-IDF Vectorization
- Cosine Similarity
- Jaccard Token Overlap
- Keyword Relevance
"""

from typing import Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nlp.text_cleaner import clean_text, tokenize_words, remove_stopwords


def calculate_tfidf_similarity(text_a: str, text_b: str) -> float:
    """
    Computes TF-IDF Cosine Similarity score between two texts.
    Returns a float between 0.0 and 100.0 (percentage).
    """
    cleaned_a = clean_text(text_a)
    cleaned_b = clean_text(text_b)

    if not cleaned_a or not cleaned_b:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        tfidf_matrix = vectorizer.fit_transform([cleaned_a, cleaned_b])
        cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        # Return percentage rounded to 2 decimal places
        return round(float(cos_sim) * 100, 2)
    except Exception:
        # Fallback to Jaccard overlap if TF-IDF fails (e.g. empty vocab)
        return calculate_jaccard_similarity(text_a, text_b)


def calculate_jaccard_similarity(text_a: str, text_b: str) -> float:
    """
    Computes Jaccard word set similarity between two texts:
    |A ∩ B| / |A ∪ B| * 100
    """
    words_a = set(remove_stopwords(tokenize_words(text_a)))
    words_b = set(remove_stopwords(tokenize_words(text_b)))

    if not words_a or not words_b:
        return 0.0

    intersection = words_a.intersection(words_b)
    union = words_a.union(words_b)

    if not union:
        return 0.0

    return round((len(intersection) / len(union)) * 100, 2)


def compute_comprehensive_match(resume_text: str, job_text: str) -> Dict[str, Any]:
    """
    Returns multi-faceted text similarity metrics between resume and job description.
    """
    tfidf_score = calculate_tfidf_similarity(resume_text, job_text)
    jaccard_score = calculate_jaccard_similarity(resume_text, job_text)

    # Combined composite similarity index
    composite_match = round((0.75 * tfidf_score) + (0.25 * jaccard_score), 2)

    return {
        "tfidf_similarity": tfidf_score,
        "jaccard_similarity": jaccard_score,
        "composite_match": composite_match,
    }
