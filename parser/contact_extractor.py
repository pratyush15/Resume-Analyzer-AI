
"""
Extract contact information from resume.
"""

import re


class ContactExtractor:

    EMAIL_PATTERN = (
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    # Covers: +91-9876543210, +91 9876543210, 9876543210, 98765 43210, (123) 456-7890
    PHONE_PATTERN = (
        r"(\+?\d{1,3}[\s\-]?)?"      # optional country code
        r"(\(?\d{3,5}\)?[\s\-]?)"    # area code or first block
        r"(\d{3,5}[\s\-]?)"          # middle block
        r"(\d{3,5})"                 # last block
    )

    LINKEDIN_PATTERN = (
        r"https?://(?:www\.)?linkedin\.com/in/[^\s]+"
    )

    GITHUB_PATTERN = (
        r"https?://(?:www\.)?github\.com/[^\s]+"
    )

    @classmethod
    def extract(cls, text: str):
        email = re.search(cls.EMAIL_PATTERN, text)
        phone = re.search(cls.PHONE_PATTERN, text)
        linkedin = re.search(cls.LINKEDIN_PATTERN, text)
        github = re.search(cls.GITHUB_PATTERN, text)

        return {
            "email": email.group().strip() if email else "",
            "phone": phone.group().strip() if phone else "",
            "linkedin": linkedin.group().strip() if linkedin else "",
            "github": github.group().strip() if github else ""
        }