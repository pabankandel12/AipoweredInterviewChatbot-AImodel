from pathlib import Path

from docx import Document


def extract_text_from_docx(file_path: str) -> str:
    """Extract all paragraph text from a .docx file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CV file not found: {file_path}")

    doc = Document(path)
    return "\n".join(para.text for para in doc.paragraphs)
