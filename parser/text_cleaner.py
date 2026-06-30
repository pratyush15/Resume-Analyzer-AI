"""
Resume Text Cleaner
"""

import re


class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:

        # Remove multiple spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Trim whitespace
        text = text.strip()

        return text