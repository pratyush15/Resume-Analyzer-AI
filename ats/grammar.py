
"""
Grammar Analyzer — with proper noun whitelisting.
"""

import language_tool_python

from ats.ats_text_cleaner import ATSTextCleaner
from models.grammar_report import GrammarReport


class GrammarAnalyzer:

    def __init__(self):
        self.tool = language_tool_python.LanguageTool("en-US")

    def analyze(self, text: str) -> GrammarReport:

        # Extract proper nouns to whitelist
        proper_nouns = ATSTextCleaner.extract_proper_nouns(text)

        matches = self.tool.check(text)

        total_errors = 0
        suggestions = []

        for match in matches:

            error_length = getattr(
                match,
                "matchedLength",
                getattr(match, "errorLength", 0)
            )

            incorrect_text = text[
                match.offset: match.offset + error_length
            ]

            if incorrect_text.strip() in proper_nouns:
                continue

            # Skip if any replacement matches a proper noun
            if match.replacements and match.replacements[0] in proper_nouns:
                continue

            # Skip single uppercase tokens — likely acronyms or names
            if incorrect_text.isupper() and len(incorrect_text) <= 5:
                continue

            total_errors += 1

            if len(suggestions) < 10:
                suggestions.append({
                    "message": match.message,
                    "incorrect": incorrect_text,
                    "replacement": (
                        match.replacements[0]
                        if match.replacements else ""
                    )
                })

        words = max(1, len(text.split()))
        error_rate = total_errors / words
        score = max(0, round(100 - (error_rate * 1000), 2))

        return GrammarReport(
            score=score,
            total_errors=total_errors,
            suggestions=suggestions
        )