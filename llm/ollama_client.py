"""
Ollama Client
"""

import ollama

from config import (
    OLLAMA_HOST,
    LLM_MODEL
)


class OllamaClient:
    
    def __init__(self):
        self.client = ollama.Client(
            host=OLLAMA_HOST
        )

    def generate(self, prompt: str):
        response = self.client.chat(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]