"""
Command-line entry point.

Fix vs. the original: the original main.py hardcoded an absolute Mac path
(`/Users/user/Desktop/paban/...`) and ignored the actual extracted CV text
in favor of a hardcoded `cv_text` string. Now the CV path and job
description are real CLI arguments.

Usage:
    python main.py --cv path/to/resume.pdf --jd "Looking for a Python developer..."
    python main.py --cv path/to/resume.pdf --jd-file job_description.txt --difficulty hard
    python main.py --cv path/to/resume.pdf --jd "..." --voice   # ask the candidate a question by voice
"""

import argparse

from ai_model.pipeline import run_pipeline
from fastapi import FastAPI, UploadFile, File, Form
import tempfile
import uuid
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware


# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# in-memory session store (use MongoDB later)
sessions = {}

def parse_args():
    parser = argparse.ArgumentParser(description="AI interview chatbot pipeline")
    parser.add_argument("--cv", required=True, help="Path to the candidate's CV (.pdf or .docx)")

    jd_group = parser.add_mutually_exclusive_group(required=True)
    jd_group.add_argument("--jd", help="Job description as a string")
    jd_group.add_argument("--jd-file", help="Path to a text file containing the job description")

    parser.add_argument(
        "--difficulty", default="medium", choices=["easy", "medium", "hard"],
        help="Difficulty of generated interview questions",
    )
    parser.add_argument(
        "--no-ai", action="store_true",
        help="Skip the Gemini call and always use template questions",
    )
    parser.add_argument(
        "--voice", action="store_true",
        help="After showing questions, record one spoken answer via the microphone",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    jd_text = args.jd
    if args.jd_file:
        with open(args.jd_file, "r", encoding="utf-8") as f:
            jd_text = f.read()

    result = run_pipeline(
        cv_path=args.cv,
        jd_text=jd_text,
        difficulty=args.difficulty,
        use_ai_questions=not args.no_ai,
    )

    print("Name:", result["name"])
    print("Skills:", result["skills"])
    print("Match Score:", result["match_score"])
    print("Questions:")
    for q in result["questions"]:
        print(" -", q)

    if args.voice:
        from ai_model.voice import voice_to_text
        print("\nAsking the first question by voice...")
        answer = voice_to_text()
        print("Candidate answer:", answer)


if __name__ == "__main__":
    main()
