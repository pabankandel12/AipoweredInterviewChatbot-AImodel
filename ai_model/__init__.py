"""
ai_model
========
A small, reusable pipeline for an AI-powered interview chatbot:

    CV (PDF/DOCX) ──► extract text ──► preprocess ──► extract skills/name
                                                              │
    Job description ──► preprocess ─────────────────────────┤
                                                              ▼
                                                  match score + interview questions

Quick start
-----------
    from ai_model.pipeline import run_pipeline

    result = run_pipeline(
        cv_path="PABAN_KANDEL.pdf",
        jd_text="Looking for a Python developer with API and ML knowledge",
    )
    print(result)
"""

__version__ = "0.1.0"
