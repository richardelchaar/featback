"""Text processing utilities."""

import re


def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    # Remove extra whitespace and normalize
    return re.sub(r'\s+', ' ', text.strip())

def extract_mentions(text: str) -> list[str]:
    """Extract @mentions from text."""
    return re.findall(r'@(\w+)', text)
