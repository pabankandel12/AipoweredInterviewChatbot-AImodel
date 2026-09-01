"""
Generates interview questions from a list of skills.

Two modes:
  - Template mode (default, no API key needed): deterministic questions
    built from simple templates. Always works offline.
  - AI mode (if GEMINI_API_KEY is set): asks Gemini to write sharper,
    more natural interview questions for the given skills + difficulty.

This fixes the original version, which ignored its `skills`/`level`
arguments entirely and just sent the literal string "Hello" to the model.
"""

from ai_model.config import GEMINI_API_KEY, GEMINI_MODEL

_TEMPLATES = {
    "easy": "What is {skill}?",
    "medium": "Explain your experience with {skill} and a project where you used it.",
    "hard": "Describe a challenging problem you solved using {skill}, and the trade-offs you considered.",
}


def _template_questions(skills, level: str) -> list:
    template = _TEMPLATES.get(level, _TEMPLATES["medium"])
    return [template.format(skill=skill) for skill in skills]


def _ai_questions(skills, level: str) -> list:
    """Ask Gemini to generate questions. Raises on any failure so the
    caller can fall back to templates."""
    from google import genai  # imported lazily so this is optional

    client = genai.Client(api_key=GEMINI_API_KEY)

    skills_list = ", ".join(skills) if skills else "general software engineering"
    prompt = (
        f"You are an interviewer. Write one concise, {level}-difficulty "
        f"interview question for each of these skills: {skills_list}. "
        "Return only the questions, one per line, no numbering."
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    lines = [line.strip("-• ").strip() for line in response.text.splitlines()]
    return [line for line in lines if line]


def generate_questions(skills, level: str = "medium", use_ai: bool = True) -> list:
    """Generate one interview question per skill.

    Args:
        skills: list of skill strings (e.g. ["python", "react"])
        level: "easy" | "medium" | "hard"
        use_ai: if True and GEMINI_API_KEY is set, try the AI path first;
                 always falls back to templates on any error or missing key.
    """
    if not skills:
        return []

    if use_ai and GEMINI_API_KEY:
        try:
            return _ai_questions(skills, level)
        except Exception as exc:  # noqa: BLE001 - we want a safe fallback, not a crash
            print(f"[question_generator] AI generation failed ({exc}); using templates.")

    return _template_questions(skills, level)
