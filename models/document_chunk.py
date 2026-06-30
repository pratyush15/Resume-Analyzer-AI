from dataclasses import dataclass


@dataclass
class DocumentChunk:
    """
    Represents a chunk stored in the FAISS index.
    """

    chunk_id: int
    text: str
    source: str