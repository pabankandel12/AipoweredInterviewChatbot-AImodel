import re

_SKIP_PATTERNS = (
    re.compile(r"@"),                      # emails
    re.compile(r"https?://|www\.|\.com"),  # urls
    re.compile(r"\d{3,}"),                  # phone numbers / long digit runs
    re.compile(r"linkedin|github|portfolio", re.IGNORECASE),
)


def extract_name(text: str) -> str:
    """Best-effort guess at the candidate's name from raw CV text.

    Fix vs. the original: the original returned the very first non-empty
    line, which breaks if the resume starts with a logo caption, an email,
    or a phone number before the name. We now skip lines that look like
    contact info and require something that resembles "First Last".
    """
    if not text:
        return "Unknown"

    for line in text.split("\n")[:10]:  # name is almost always near the top
        line = line.strip()
        if not line:
            continue
        if any(p.search(line) for p in _SKIP_PATTERNS):
            continue

        word_count = len(line.split())
        if 2 <= word_count <= 4:
            return line

    return "Unknown"
