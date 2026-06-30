
"""
Semantic similarity utilities.
"""

import numpy as np
from embeddings.embedder import Embedder


class SimilarityCalculator:

    def __init__(self):
        self.embedder = Embedder()

    @staticmethod
    def cosine_similarity(vec1, vec2):
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        denominator = (
            np.linalg.norm(vec1) *
            np.linalg.norm(vec2)
        )

        if denominator == 0:
            return 0.0

        similarity = np.dot(vec1, vec2) / denominator

        return round(float(similarity), 4)

    def compare(self, text1: str, text2: str):
        emb1 = self.embedder.embed(text1)
        emb2 = self.embedder.embed(text2)

        return self.cosine_similarity(emb1, emb2)