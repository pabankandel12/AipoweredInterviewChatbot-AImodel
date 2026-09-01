import json
from ai_model.config import GEMINI_API_KEY, GEMINI_MODEL

def evaluate_answer(question: str, answer: str, jd: str, difficulty: str) -> dict:
    """Evaluate a candidate's answer to a question in the context of the job description.

    Returns a dict with:
        - "feedback": constructive feedback text
        - "score": score from 0 to 100 (int)
    """
    if not GEMINI_API_KEY:
        # Fallback if no API key
        return {
            "feedback": "Gemini API key is not configured. Automated evaluation is unavailable. Answers are marked with a default passing score.",
            "score": 70
        }

    from google import genai

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = (
        "You are an expert technical interviewer. Evaluate the candidate's answer to the following question. "
        "Consider the job description and the difficulty level of the interview.\n\n"
        f"Job Description: {jd}\n"
        f"Difficulty Level: {difficulty}\n"
        f"Question: {question}\n"
        f"Candidate's Answer: {answer}\n\n"
        "Provide constructive, professional feedback (highlighting strengths and areas of improvement in 2-3 sentences) and a numerical score out of 100.\n"
        "Return your response strictly in JSON format. Do not include any markdown code blocks or extra text outside the JSON. The JSON must have exactly these keys:\n"
        '{\n  "feedback": "string",\n  "score": integer\n}'
    )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        text = response.text.strip()
        
        # Clean up markdown code blocks if Gemini returns them
        if text.startswith("```"):
            lines = text.splitlines()
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()

        data = json.loads(text)
        feedback = data.get("feedback", "No feedback provided.")
        score = data.get("score", 70)
        try:
            score = int(score)
        except ValueError:
            score = 70

        return {
            "feedback": feedback,
            "score": score
        }
    except Exception as e:
        print(f"[evaluator] Gemini evaluation failed: {e}")
        return {
            "feedback": f"Evaluation could not be processed due to an error: {str(e)}",
            "score": 50
        }
