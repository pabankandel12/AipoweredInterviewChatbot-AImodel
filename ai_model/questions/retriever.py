from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .question_bank import QUESTION_BANK


def retrieve_questions(jd_text: str, skills: list[str], level: str, limit: int = 5) -> list[dict]:
    """Retrieve relevant question records from the local knowledge base with TF-IDF.

    This is the retrieval step of the project's RAG design. Each returned
    record provides a question plus the rubric used to ground evaluation.
    """
    query = " ".join([jd_text, *skills]).strip() or "general interview"
    documents = [f"{item['skill']} {item['level']} {item['question']} {item['rubric']}" for item in QUESTION_BANK]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([query, *documents])
    scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    ranked = sorted(
        enumerate(QUESTION_BANK),
        key=lambda item: (item[1]["level"] == level, scores[item[0]]),
        reverse=True,
    )
    selected = []
    selected_skills = set()
    for index, item in ranked:
        if item["skill"] in selected_skills and item["skill"] != "general":
            continue
        selected.append({**item, "retrieval_score": round(float(scores[index]), 3)})
        selected_skills.add(item["skill"])
        if len(selected) == limit:
            break
    return selected
