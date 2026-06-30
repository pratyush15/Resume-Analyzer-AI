from dataclasses import dataclass
from models.resume import Resume


@dataclass
class ResumeProcessingResult:
    resume: Resume
    chunks: list
    embeddings: list
    faiss_ready: bool