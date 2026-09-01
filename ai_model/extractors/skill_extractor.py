DEFAULT_SKILLS_DB = [
    "python", "java", "javascript", "typescript", "react", "react.js",
    "node", "node.js", "express.js", "mern stack", "django", "flask",
    "php", "dot net", ".net",
    "mysql", "postgresql", "mongodb",
    "aws", "azure", "docker", "git", "vercel", "netlify",
    "machine learning", "nlp", "nltk", "api",
]


def extract_skills(text: str, skills_db=None) -> list:
    """Return the subset of `skills_db` found anywhere in `text`.

    `skills_db` is now an optional parameter (defaults to DEFAULT_SKILLS_DB)
    so callers can plug in a domain-specific skill list instead of editing
    this file directly.
    """
    skills_db = skills_db or DEFAULT_SKILLS_DB
    text_lower = text.lower()
    found = {skill for skill in skills_db if skill in text_lower}
    return sorted(found)
