"""
Split text into overlapping chunks.
"""

from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

class TextChunker:

    @staticmethod
    def chunk(text: str):
        chunks = []
        start = 0
        while start < len(text):
            end = start + CHUNK_SIZE
            chunks.append(text[start:end])
            start += CHUNK_SIZE - CHUNK_OVERLAP

        return chunks