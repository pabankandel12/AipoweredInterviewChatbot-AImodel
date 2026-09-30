from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_details(cv: str, jd: str) -> dict:
    """Calculate TF-IDF cosine similarity and return its shared-term evidence."""
    if not cv.strip() or not jd.strip():
        return {"score": 0.0, "shared_terms": []}

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    vectors = vectorizer.fit_transform([cv, jd])
    similarity = float(cosine_similarity(vectors[0:1], vectors[1:2])[0][0])

    feature_names = vectorizer.get_feature_names_out()
    term_weights = vectors[0].multiply(vectors[1]).toarray()[0]
    top_indexes = term_weights.argsort()[::-1]
    shared_terms = [
        feature_names[index]
        for index in top_indexes
        if term_weights[index] > 0
    ][:8]

    return {"score": round(similarity, 2), "shared_terms": shared_terms}


def calculate_match(cv: str, jd: str) -> float:
    """Backward-compatible TF-IDF cosine similarity score between 0 and 1."""
    return calculate_match_details(cv, jd)["score"]
