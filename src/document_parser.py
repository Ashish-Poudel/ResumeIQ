
from pathlib import Path

import pymupdf  # PyMuPDF: extracts text from PDF files
from docx import Document  # Reads Microsoft Word DOCX files


def extract_text(file_path: str | Path) -> str:
    """
    Extract text from a PDF or DOCX resume.

    Args:
        file_path: Path to the resume file.

    Returns:
        Extracted text as a string.

    Raises:
        ValueError: If the file type is unsupported or no text is found.
    """

    # Convert the input path into a Path object.
    # This makes file paths easier to work with.
    path = Path(file_path)

    # Check that the resume actually exists.
    if not path.is_file():
        raise FileNotFoundError(f"Resume file not found: {path}")

    # Identify the document format from its extension.
    extension = path.suffix.lower()

    if extension == ".pdf":
        # Open the PDF and extract text from each page.
        with pymupdf.open(path) as pdf:
            pages = [page.get_text() for page in pdf]

        text = "\n".join(pages)

    elif extension == ".docx":
        # Open the Word document and extract paragraph text.
        document = Document(path)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        text = "\n".join(paragraphs)

    else:
        raise ValueError(
            "Unsupported file format. Please use PDF or DOCX."
        )

    # Scanned PDFs may contain images instead of selectable text.
    # This initial version requires text that can be extracted directly.
    if not text.strip():
        raise ValueError(
            "No readable text found. The document may be scanned "
            "or empty."
        )

    return text
