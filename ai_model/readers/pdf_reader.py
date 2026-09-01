from pathlib import Path

import PyPDF2


def extract_text_from_pdf(file_path: str) -> str:
    """Extract all text from a PDF file.

    Fixes vs. the original version:
      - Guards against `page.extract_text()` returning None (happens on
        image-only / oddly-encoded pages), which previously crashed with
        `TypeError: can only concatenate str (not "NoneType") to str`.
      - Raises a clear FileNotFoundError instead of a cryptic one if the
        path is wrong.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CV file not found: {file_path}")

    text_parts = []
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")

    return "\n".join(text_parts)
