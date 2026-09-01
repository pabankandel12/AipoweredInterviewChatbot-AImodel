from pathlib import Path

from .pdf_reader import extract_text_from_pdf
from .docx_reader import extract_text_from_docx

__all__ = ["extract_text_from_pdf", "extract_text_from_docx", "extract_text"]


def extract_text(file_path: str) -> str:
    """Dispatch to the right reader based on file extension."""
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    if ext == ".docx":
        return extract_text_from_docx(file_path)
    raise ValueError(f"Unsupported CV file type: {ext} (use .pdf or .docx)")
