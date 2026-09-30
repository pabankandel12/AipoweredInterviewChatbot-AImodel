"""Grounded question generation with retrieval-first offline fallback."""

from ai_model.config import GEMINI_API_KEY, GEMINI_MODEL


def _ai_questions(skills: list[str], level: str, retrieved_questions: list[dict]) -> list[str]:
    from google import genai

    client = genai.Client(api_key=GEMINI_API_KEY)
    context = "\n".join(f"- {item['question']}" for item in retrieved_questions)
    prompt = (
        "You are an interviewer. Use only the retrieved interview-question context below "
        f"to write up to {len(retrieved_questions)} concise {level}-difficulty questions. "
        f"Candidate skills: {', '.join(skills) or 'general software development'}.\n"
        f"Retrieved context:\n{context}\nReturn only questions, one per line, no numbering."
    )
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    return [line.strip("-• ").strip() for line in response.text.splitlines() if line.strip()]


def generate_questions(skills: list[str], level: str = "medium", retrieved_questions: list[dict] | None = None, use_ai: bool = True) -> list[str]:
    """Generate questions grounded in retrieved records; always returns a fallback set."""
    retrieved_questions = retrieved_questions or []
    if use_ai and GEMINI_API_KEY and retrieved_questions:
        try:
            generated = _ai_questions(skills, level, retrieved_questions)
            if generated:
                return generated[: len(retrieved_questions)]
        except Exception as exc:  # noqa: BLE001
            print(f"[question_generator] AI generation failed ({exc}); using retrieved questions.")

    questions = [item["question"] for item in retrieved_questions]
    if questions:
        return questions

    return [
        "Tell me about a project you are proud of and the contribution you made.",
        "Describe a challenging problem you solved and the steps you took.",
        "What would you like to improve in your next technical role?",
    ]
