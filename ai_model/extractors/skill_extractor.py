import re

# Canonical skill names and the common forms found in CVs and job descriptions.
SKILL_ALIASES = {
    "python": ("python",),
    "java": ("java",),
    "javascript": ("javascript", "js"),
    "typescript": ("typescript", "ts"),
    "react": ("react", "react.js", "reactjs"),
    "node.js": ("node", "node.js", "nodejs"),
    "express": ("express", "express.js", "expressjs"),
    "django": ("django",),
    "flask": ("flask",),
    "mongodb": ("mongodb", "mongo db"),
    "mysql": ("mysql",),
    "postgresql": ("postgresql", "postgres"),
    "rest api": ("rest api", "restful api", "api development"),
    "docker": ("docker",),
    "git": ("git", "github"),
    "aws": ("aws", "amazon web services"),
    "machine learning": ("machine learning", "ml"),
    "natural language processing": ("natural language processing", "nlp"),
    "data analysis": ("data analysis", "data analytics"),
}

DEFAULT_SKILLS_DB = list(SKILL_ALIASES)


def _contains_phrase(text: str, phrase: str) -> bool:
    return bool(re.search(r"(?<![a-z0-9])" + re.escape(phrase.lower()) + r"(?![a-z0-9])", text))


def extract_skills(text: str, skills_db=None) -> list[str]:
    """Extract canonical skills from one source document.

    CV and job-description skills must be extracted independently. Combining
    both sources falsely credits a candidate with skills that only appear in a
    vacancy advertisement.
    """
    if not text:
        return []

    text_lower = text.lower()
    if skills_db is not None:
        return sorted(skill for skill in skills_db if _contains_phrase(text_lower, skill))

    found = [
        canonical
        for canonical, aliases in SKILL_ALIASES.items()
        if any(_contains_phrase(text_lower, alias) for alias in aliases)
    ]
    return sorted(found)
