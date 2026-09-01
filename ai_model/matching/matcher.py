from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match(cv: str, jd: str) -> float:
    """TF-IDF cosine similarity between a CV and a job description.

    Returns a score between 0.0 and 1.0.
    """
    if not cv.strip() or not jd.strip():
        return 0.0

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([cv, jd])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(float(similarity[0][0]), 2)
