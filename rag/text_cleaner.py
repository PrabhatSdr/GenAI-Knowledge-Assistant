import re


def clean_text(text: str) -> str:
    """
    Cleans extracted document text.

    Steps:
    1. Remove extra spaces
    2. Remove multiple blank lines
    3. Normalize whitespace
    """

    # Remove multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text