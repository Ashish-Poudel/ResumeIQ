import re

def clean_text(text: str) -> str:
    """
    Clean extracted resume or job-description text.

    Args:
        text: Raw text extracted from a document.

    Returns:
        Text with extra whitespace removed and converted to lowercase.
    """

    # Converting text to lowercase so Python treats
    
    text = text.lower()

    # Replace one or more whitespace characters
    # (spaces, tabs, newlines) with a single space.
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary spaces from the beginning
    # and end of the text.
    text = text.strip()

    return text
