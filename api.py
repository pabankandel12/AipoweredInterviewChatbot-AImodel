from fastapi import FastAPI, UploadFile, File, Form, HTTPException
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
    temp_path = None
    try:
        if difficulty not in {"easy", "medium", "hard"}:
            raise HTTPException(status_code=422, detail="difficulty must be easy, medium, or hard")
        if not cv.filename or not cv.filename.lower().endswith((".pdf", ".docx")):
            raise HTTPException(status_code=415, detail="Only PDF and DOCX resume files are supported")
        # Save uploaded CV to a temporary file
        suffix = ".pdf"
        if cv.filename and cv.filename.endswith(".docx"):
            suffix = ".docx"
            
        content = await cv.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Resume file must be 10MB or smaller")
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
            temp.write(content)
            temp_path = temp.name

        # Run the parsing, matching, and question generation pipeline
        result = run_pipeline(
            cv_path=temp_path,
            jd_text=jd,
            difficulty=difficulty,
            use_ai_questions=True,
        )

        return result  # Returns: { name, skills, match_score, questions }

    except HTTPException:
        raise
    except Exception as e:
        print("🔥 /interview error:", str(e))
        raise HTTPException(status_code=500, detail="Interview analysis failed") from e
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


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
            raise HTTPException(status_code=422, detail="question and answer are required")

        # Run AI-powered answer evaluation
        result = evaluate_answer(
            question=question,
            answer=answer,
            jd=jd,
            difficulty=difficulty
        )

        return result  # Returns: { feedback, score }

    except HTTPException:
        raise
    except Exception as e:
        print("🔥 /evaluate error:", str(e))
        raise HTTPException(status_code=500, detail="Answer evaluation failed") from e


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "AI Interview Parser Microservice"}
