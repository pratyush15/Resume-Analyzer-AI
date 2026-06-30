
"""
FAISS Vector Database Manager

Two index types:
- FAISSVectorDB     — IndexFlatL2, used by RAG / Chat / Interview
- ATSFAISSVectorDB  — IndexFlatIP + L2 normalization, used by ATS scorer (cosine similarity)
"""

import pickle

import faiss
import numpy as np

from config import (
    FAISS_INDEX_PATH,
    FAISS_METADATA_PATH
)

from models.document_chunk import DocumentChunk


# -----------------------------------------------------------------------
# Standard FAISS — L2 distance, used by RAG pipeline
# -----------------------------------------------------------------------

class FAISSVectorDB:

    def __init__(self):
        self.index = None
        self.metadata = []

    def create_index(self, dimension: int):
        """
        Create a new IndexFlatL2 index.
        """
        self.index = faiss.IndexFlatL2(dimension)

    def add_documents(
        self,
        embeddings: list,
        documents: list[DocumentChunk]
    ):
        vectors = np.array(embeddings, dtype=np.float32)
        self.index.add(vectors)
        self.metadata.extend(documents)

    def save(self):
        FAISS_INDEX_PATH.parent.mkdir(exist_ok=True)

        faiss.write_index(self.index, str(FAISS_INDEX_PATH))

        with open(FAISS_METADATA_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))

        with open(FAISS_METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, embedding, top_k=5) -> list:
        """
        Returns list of chunks (plain, no scores).
        """
        query = np.array([embedding], dtype=np.float32)

        distances, indices = self.index.search(query, top_k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.metadata[idx])

        return results


# -----------------------------------------------------------------------
# ATS FAISS — IndexFlatIP + L2 normalization, cosine similarity scoring
# -----------------------------------------------------------------------

class ATSFAISSVectorDB:

    def __init__(self):
        self.index = None
        self.metadata = []

    def create_index(self, dimension: int):
        """
        Create IndexFlatIP index.
        Vectors must be L2-normalized before adding
        so inner product equals cosine similarity.
        """
        self.index = faiss.IndexFlatIP(dimension)

    def _normalize(self, vectors: np.ndarray) -> np.ndarray:
        faiss.normalize_L2(vectors)
        return vectors

    def add_documents(
        self,
        embeddings: list,
        documents: list[DocumentChunk]
    ):
        vectors = np.array(embeddings, dtype=np.float32)
        vectors = self._normalize(vectors)
        self.index.add(vectors)
        self.metadata.extend(documents)

    def save(self):
        FAISS_INDEX_PATH.parent.mkdir(exist_ok=True)

        faiss.write_index(self.index, str(FAISS_INDEX_PATH))

        with open(FAISS_METADATA_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def load(self):
        self.index = faiss.read_index(str(FAISS_INDEX_PATH))

        with open(FAISS_METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, embedding, top_k: int = 5) -> list:
        """
        Returns list of (chunk, cosine_score) tuples.
        Scores are between 0 and 1.
        """
        query = np.array([embedding], dtype=np.float32)
        faiss.normalize_L2(query)

        scores, indices = self.index.search(query, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.metadata[idx], float(score)))

        return results