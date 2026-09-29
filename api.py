from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os
from typing import Dict, Any

from ai_model.pipeline import run_pipeline
from ai_model.questions import evaluate_answer

app = FastAPI()

# The frontend origins are configured in .env locally and as CORS_ORIGINS in
# Render's environment settings. Separate multiple origins with commas.
cors_origins = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# START INTERVIEW / ANALYZE CV & JD
# -----------------------------
@app.post("/interview")
async def generate_interview(
    cv: UploadFile = File(...),
    jd: str = Form(...),
    difficulty: str = Form("medium"),
):
    try:
        # Save uploaded CV to a temporary file
        suffix = ".pdf"
        if cv.filename and cv.filename.endswith(".docx"):
            suffix = ".docx"
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(await cv.read())
            temp_path = temp.name

        # Run the parsing, matching, and question generation pipeline
        result = run_pipeline(
            cv_path=temp_path,
            jd_text=jd,
            difficulty=difficulty,
            use_ai_questions=True,
        )

        # Clean up the temporary file
        try:
            os.unlink(temp_path)
        except Exception as pe:
            print(f"⚠️ Failed to delete temp file {temp_path}: {pe}")

        return result  # Returns: { name, skills, match_score, questions }

    except Exception as e:
        print("🔥 /interview error:", str(e))
        return {"error": str(e)}


# -----------------------------
# EVALUATE SINGLE ANSWER
# -----------------------------
@app.post("/evaluate")
async def evaluate_candidate_answer(data: dict):
    try:
        question = data.get("question")
        answer = data.get("answer")
        jd = data.get("jd", "")
        difficulty = data.get("difficulty", "medium")

        if not question or not answer:
            return {"error": "question and answer are required"}

        # Run AI-powered answer evaluation
        result = evaluate_answer(
            question=question,
            answer=answer,
            jd=jd,
            difficulty=difficulty
        )

        return result  # Returns: { feedback, score }

    except Exception as e:
        print("🔥 /evaluate error:", str(e))
        return {"error": str(e)}


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "AI Interview Parser Microservice"}
