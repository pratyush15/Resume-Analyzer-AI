"""
Generate embeddings using Ollama.
"""

import ollama

from config import (
    OLLAMA_HOST,
    EMBEDDING_MODEL
)


class Embedder:

    def __init__(self):
        self.client = ollama.Client(
            host=OLLAMA_HOST
        )

    def embed(self, text: str):
        response = self.client.embed(
            model=EMBEDDING_MODEL,
            input=text
        )

        return response["embeddings"][0]