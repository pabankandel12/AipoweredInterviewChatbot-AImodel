"""
The end-to-end pipeline: CV + job description -> name, skills, match score,
interview questions.
"""

from ai_model.readers import extract_text
from ai_model.preprocessing import preprocess
from ai_model.extractors import extract_name, extract_skills
from ai_model.matching import calculate_match
from ai_model.questions import generate_questions


def run_pipeline(cv_path: str, jd_text: str, difficulty: str = "medium", use_ai_questions: bool = True) -> dict:
    """Run the full pipeline and return a single result dict.

    Args:
        cv_path: path to a .pdf or .docx resume
        jd_text: the job description text
        difficulty: "easy" | "medium" | "hard" for generated questions
        use_ai_questions: whether to try Gemini for questions (falls back
            to templates automatically if no key/connection)
    """
    cv_raw = extract_text(cv_path)

    cv_clean = preprocess(cv_raw)
    jd_clean = preprocess(jd_text)

    name = extract_name(cv_raw)
    skills = extract_skills(cv_clean + " " + jd_clean)
    score = calculate_match(cv_clean, jd_clean)
    questions = generate_questions(skills, level=difficulty, use_ai=use_ai_questions)

    return {
        "name": name,
        "skills": skills,
        "match_score": score,
        "questions": questions,
    }
