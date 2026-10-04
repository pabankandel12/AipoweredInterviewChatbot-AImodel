import json
import re

from ai_model.config import GEMINI_API_KEY, GEMINI_MODEL


def _feedback_text(value: object) -> str:
    """Turn a model response into one readable feedback paragraph.

    Gemini normally returns a string, but can occasionally return an object
    with sections such as ``overall`` and ``improvements``. Rendering that
    object directly made the chat UI show Python/JSON syntax.
    """
    if isinstance(value, str):
        return value.strip() or "No feedback provided."
    if isinstance(value, dict):
        preferred = ("overall", "feedback", "strengths", "improvements", "suggestions")
        parts = [str(value[key]).strip() for key in preferred if value.get(key)]
        if not parts:
            parts = [str(item).strip() for item in value.values() if item]
        return " ".join(parts) or "No feedback provided."
    if isinstance(value, list):
        return " ".join(str(item).strip() for item in value if item) or "No feedback provided."
    return "No feedback provided."


def _rubric_evaluation(question: str, answer: str, jd: str) -> dict:
    """Explainable offline score based on detail, relevance, and evidence."""
    answer_words = re.findall(r"[a-zA-Z]{3,}", answer.lower())
    reference_words = set(re.findall(r"[a-zA-Z]{3,}", f"{question} {jd}".lower()))
    relevant_words = {word for word in answer_words if word in reference_words}
    completeness = min(40, len(answer_words) * 2)
    relevance = min(35, len(relevant_words) * 5)
    evidence_terms = {"built", "used", "improved", "result", "because", "challenge", "tested"}
    evidence = min(25, len(set(answer_words) & evidence_terms) * 4)
    score = completeness + relevance + evidence
    suggestions = []
    if completeness < 24:
        suggestions.append("Add more detail about your approach and outcome.")
    if relevance < 15:
        suggestions.append("Connect the answer more directly to the question and job requirements.")
    if evidence < 12:
        suggestions.append("Include a concrete example, your role, and a measurable result.")
    return {
        "feedback": " ".join(suggestions) or "Clear answer with relevant detail and a practical example.",
        "score": score,
        "evaluation_mode": "transparent_rubric",
    }


def evaluate_answer(question: str, answer: str, jd: str, difficulty: str) -> dict:
    if not GEMINI_API_KEY:
        return _rubric_evaluation(question, answer, jd)
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = (
            "You are an expert technical interviewer. Evaluate this answer. Return strict JSON "
            "with exactly two fields: feedback (a concise plain-text paragraph of 2 to 4 sentences) "
            "and score (an integer from 0 to 100). Do not return nested objects, lists, headings, "
            "or markdown.\n\n"
            f"Job Description: {jd}\nDifficulty: {difficulty}\nQuestion: {question}\nAnswer: {answer}"
        )
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        text = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(text)
        score = int(float(data.get("score", 0)))
        return {
            "feedback": _feedback_text(data.get("feedback")),
            "score": max(0, min(100, score)),
            "evaluation_mode": "gemini",
        }
    except Exception as error:  # noqa: BLE001
        print(f"[evaluator] Gemini evaluation failed: {error}; using transparent rubric.")
        return _rubric_evaluation(question, answer, jd)
