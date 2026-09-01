"""
Centralized configuration.

NEVER hardcode API keys in source files. This module loads them from
environment variables (optionally via a local .env file using python-dotenv).

Setup:
    1. Copy `.env.example` to `.env`
    2. Put your real key in `.env`:  GEMINI_API_KEY=your-real-key-here
    3. `.env` should be in your .gitignore so it never gets committed.
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed -- fine, we just rely on real env vars.
    pass

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")


def require_gemini_key() -> str:
    """Return the Gemini API key, or raise a clear error if it's missing."""
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Create a .env file (see .env.example) "
            "or export GEMINI_API_KEY in your shell."
        )
    return GEMINI_API_KEY
