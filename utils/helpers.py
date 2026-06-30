"""
General helper utilities.
"""

from pathlib import Path
import re
from datetime import datetime


def sanitize_filename(filename: str) -> str:
    """
    Remove special characters from filename.
    """
    name = Path(filename).stem
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "_", name).strip()
    return name


def get_timestamp() -> str:
    """
    Return current timestamp as a string.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def truncate_text(text: str, max_chars: int = 500) -> str:
    """
    Truncate text to a maximum number of characters.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "..."


def word_count(text: str) -> int:
    """
    Return word count of a string.
    """
    return len(text.split())


def format_score(score: float) -> str:
    """
    Format a float score as a percentage string.
    """
    return f"{round(score, 1)}%"