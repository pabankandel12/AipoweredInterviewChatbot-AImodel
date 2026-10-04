"""
The end-to-end pipeline: CV + job description -> name, skills, match score,
interview questions.
"""

from ai_model.readers import extract_text
from ai_model.preprocessing import preprocess
from ai_model.extractors import extract_name, extract_skills
from ai_model.matching import calculate_match_details
from ai_model.questions import generate_questions, retrieve_questions


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
    candidate_skills = extract_skills(cv_raw)
    required_skills = extract_skills(jd_text)
    matched_skills = sorted(set(candidate_skills) & set(required_skills))
    missing_skills = sorted(set(required_skills) - set(candidate_skills))
    match_details = calculate_match_details(cv_clean, jd_clean)
    retrieved_questions = retrieve_questions(jd_text, matched_skills or required_skills, difficulty)
    questions = generate_questions(
        matched_skills or required_skills,
        level=difficulty,
        retrieved_questions=retrieved_questions,
        use_ai=use_ai_questions,
    )

    return {
        "name": name,
        "skills": candidate_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": match_details["score"],
        "shared_terms": match_details["shared_terms"],
        "questions": questions,
        "retrieved_questions": retrieved_questions,
    }
