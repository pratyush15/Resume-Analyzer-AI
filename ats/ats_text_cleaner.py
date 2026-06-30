"""
ATS Text Cleaner — strips noise from JD and resume text
before keyword matching and FAISS vectorization.

Implements:
1. Custom ATS stopwords (corporate buzzwords)
2. POS filtering via spaCy (keep only nouns + proper nouns)
"""

import re
import spacy

# Load spaCy model — small English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError(
        "spaCy model not found. Run: python -m spacy download en_core_web_sm"
    )

# Custom ATS stopwords — corporate boilerplate that adds no signal
ATS_STOPWORDS = {
    # Action verbs
    "integrate", "participate", "collaborate", "communicate", "coordinate",
    "deliver", "develop", "drive", "enable", "engage", "ensure", "execute",
    "facilitate", "implement", "improve", "join", "lead", "leverage",
    "maintain", "manage", "mentor", "optimize", "oversee", "own",
    "partner", "perform", "prioritize", "provide", "require", "resolve",
    "scale", "shape", "ship", "support", "translate", "work", "build",
    "create", "design", "define", "identify", "establish", "contribute",

    # JD boilerplate phrases / fragments
    "looking", "required", "requirements", "responsibilities", "candidate",
    "role", "team", "successful", "plus", "preferred", "excellent",
    "strong", "ability", "opportunity", "environment", "culture",
    "mission", "passionate", "excited", "bonus", "ideal", "seeking",
    "hire", "position", "opening", "apply", "applicant", "employer",
    "company", "organization", "startup", "enterprise", "firm",

    # Pronouns / fillers
    "we", "our", "us", "you", "your", "they", "their", "it", "its",
    "what", "who", "how", "why", "when", "where", "which",
    "this", "that", "these", "those", "there", "here",

    # Generic adjectives
    "good", "great", "fast", "smart", "clean", "clear", "deep",
    "high", "low", "large", "small", "real", "new", "old",
    "key", "core", "main", "top", "best", "full", "open",
}


class ATSTextCleaner:

    @staticmethod
    def clean_for_matching(text: str) -> str:
        """
        Full cleaning pipeline for ATS keyword matching:
        1. Lowercase and normalize whitespace
        2. Remove punctuation noise
        3. Strip ATS stopwords
        4. POS filter — keep only NOUN and PROPN tokens
        Returns cleaned string.
        """

        # Step 1 — basic normalization
        text = text.replace("\r", " ").replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()

        # Step 2 — spaCy POS tagging
        doc = nlp(text)

        # Keep only nouns and proper nouns, skip ATS stopwords
        kept_tokens = []

        for token in doc:
            # Skip punctuation, spaces, numbers-only tokens
            if token.is_punct or token.is_space:
                continue

            token_lower = token.text.lower()

            # Skip ATS stopwords
            if token_lower in ATS_STOPWORDS:
                continue

            # Skip spaCy stopwords (the, is, are, etc.)
            if token.is_stop:
                continue

            # Keep NOUN and PROPN only
            if token.pos_ in ("NOUN", "PROPN"):
                kept_tokens.append(token.text)

        return " ".join(kept_tokens)

    @staticmethod
    def extract_proper_nouns(text: str) -> set:
        """
        Extract all proper nouns from text.
        Used to build a whitelist for grammar checker
        so names like 'Pratyush Jha' are not flagged.
        """
        doc = nlp(text)

        proper_nouns = set()

        for ent in doc.ents:
            # PERSON, ORG, GPE (location), PRODUCT
            if ent.label_ in ("PERSON", "ORG", "GPE", "PRODUCT"):
                proper_nouns.add(ent.text)
                # Also add individual tokens of multi-word entities
                for token in ent:
                    proper_nouns.add(token.text)

        # Also grab standalone PROPN tokens
        for token in doc:
            if token.pos_ == "PROPN":
                proper_nouns.add(token.text)

        return proper_nouns