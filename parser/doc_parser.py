"""
DOCX Resume Parser
"""

from docx import Document


class DOCParser:

    @staticmethod
    def extract_text(file_path):

        document = Document(file_path)
        paragraphs = []
        for para in document.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)

        return "\n".join(paragraphs)