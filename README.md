# AI Interview Chatbot — Model Pipeline

A reusable pipeline that takes a candidate's CV and a job description, then
produces: extracted name, matched skills, a match score, and interview
questions (AI-generated via Gemini, or template-based offline).

## Structure

```
interview_chatbot/
├── main.py                     # CLI entry point
├── requirements.txt
├── .env.example                # copy to .env and add your real API key
└── ai_model/
    ├── config.py                # loads GEMINI_API_KEY from environment
    ├── pipeline.py               # run_pipeline() — wires everything together
    ├── readers/                  # extract_text() from .pdf / .docx
    │   ├── pdf_reader.py
    │   └── docx_reader.py
    ├── preprocessing/
    │   └── preprocess.py          # lowercase, strip punctuation, remove stopwords
    ├── extractors/
    │   ├── name_extractor.py      # guesses candidate name from CV text
    │   └── skill_extractor.py     # finds known skills mentioned in text
    ├── matching/
    │   └── matcher.py             # TF-IDF cosine similarity, CV vs JD
    ├── questions/
    │   └── question_generator.py  # AI questions (Gemini) with template fallback
    └── voice/
        └── input_voice.py         # microphone -> text, only runs when called
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env and put your real Gemini key in GEMINI_API_KEY
```

## Usage

```bash
python main.py --cv resume.pdf --jd "Looking for a Python developer with API and ML knowledge"

# or read the JD from a file
python main.py --cv resume.pdf --jd-file jd.txt --difficulty hard

# skip the Gemini call entirely and just use templates
python main.py --cv resume.pdf --jd "..." --no-ai

# also record one spoken answer via microphone after showing questions
python main.py --cv resume.pdf --jd "..." --voice
```

Or use it as a library:

```python
from ai_model.pipeline import run_pipeline

result = run_pipeline(cv_path="resume.pdf", jd_text="Looking for a Python developer...")
print(result)
# {'name': 'PABAN KANDEL', 'skills': [...], 'match_score': 0.34, 'questions': [...]}
```

## What changed from the original code

| Issue | Fix |
|---|---|
| API key hardcoded in `question_generator.py` | Loaded from `.env` via `config.py`; **rotate your old key, it was exposed** |
| `generate_questions()` ignored `skills`/`level`, always sent `"Hello"` | Rebuilt to use both, with a real Gemini prompt and an offline template fallback |
| `main.py`/`test.py` used a hardcoded Mac path | CLI now takes `--cv` / `--jd` / `--jd-file` arguments |
| `Input_voice.py` called `voice_to_text()` at import time | Moved into a function, only runs when called or via `--voice` flag |
| `preprocess.py` could crash with `LookupError` if NLTK stopwords weren't downloaded | Auto-downloads once, caches the set |
| `PDFReader.py` could crash if `extract_text()` returned `None` on a page | Guarded with `or ""` |
| `name_extractor.py` returned the first non-empty line, breaking on resumes with contact info first | Skips lines that look like emails/phones/URLs, looks for a 2-4 word line |
| Everything was loose files with no package structure | Organized into `ai_model/` submodules with clear responsibilities |

## Notes

- `skill_extractor.py`'s `DEFAULT_SKILLS_DB` is a simple keyword list — extend it or pass your own list to `extract_skills(text, skills_db=...)` as your needs grow.
- `match_score` is TF-IDF cosine similarity (0–1), not a semantic match — fine as a baseline, but consider embeddings (e.g. `sentence-transformers`) later for better accuracy.
# AipoweredInterviewChatbot-AImodel
