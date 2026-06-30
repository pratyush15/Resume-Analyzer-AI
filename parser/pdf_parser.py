"""
PDF Resume Parser
"""

import fitz

class PDFParser:

    @staticmethod
    def extract_text(file_path):
        document = fitz.open(file_path)
        pages = []
        
        for page in document:
            pages.append(page.get_text())

        document.close()

        return "\n".join(pages)