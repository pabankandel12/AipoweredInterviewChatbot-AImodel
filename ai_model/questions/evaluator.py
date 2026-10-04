import json
import re

from ai_model.config import GEMINI_API_KEY, GEMINI_MODEL


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
            "with feedback and an integer score from 0 to 100.\n\n"
            f"Job Description: {jd}\nDifficulty: {difficulty}\nQuestion: {question}\nAnswer: {answer}"
        )
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        text = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        data = json.loads(text)
        return {"feedback": str(data.get("feedback", "No feedback provided.")), "score": max(0, min(100, int(data.get("score", 0)))), "evaluation_mode": "gemini"}
    except Exception as error:  # noqa: BLE001
        print(f"[evaluator] Gemini evaluation failed: {error}; using transparent rubric.")
        return _rubric_evaluation(question, answer, jd)
