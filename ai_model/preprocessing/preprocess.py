import re

import nltk
from nltk.corpus import stopwords

_STOPWORDS = None


def _get_stopwords():
    """Lazily load + cache the English stopword set.

    Fix vs. the original: the original called `stopwords.words('english')`
    on every single call with no guarantee the NLTK data was downloaded,
    which raises a LookupError on a fresh machine. We now auto-download
    once (quietly) and cache the result so repeated calls are cheap.
    """
    global _STOPWORDS
    if _STOPWORDS is None:
        try:
            _STOPWORDS = set(stopwords.words("english"))
        except LookupError:
            nltk.download("stopwords", quiet=True)
            _STOPWORDS = set(stopwords.words("english"))
    return _STOPWORDS


def preprocess(text: str) -> str:
    """Lowercase, strip punctuation, and remove English stopwords."""
    if not text:
        return ""

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())
    words = text.split()
    words = [w for w in words if w not in _get_stopwords()]
    return " ".join(words)
