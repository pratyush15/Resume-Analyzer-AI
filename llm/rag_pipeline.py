from embeddings.embedder import Embedder
from embeddings.faiss_db import FAISSVectorDB

from llm.prompts import build_prompt
from llm.ollama_client import OllamaClient

from config import TOP_K

class RAGPipeline:

    def __init__(self):
        self.embedder = Embedder()
        self.db = FAISSVectorDB()
        self.db.load()
        self.llm = OllamaClient()
        
        
    def retrieve_context(
        self,
        question
    ):
        embedding = self.embedder.embed(question)
        chunks = self.db.search(
            embedding,
            top_k=TOP_K
        )

        return "\n\n".join(
            chunk.text
            for chunk in chunks
        )
        
    def ask(
        self,
        question
    ):
        context = self.retrieve_context(question)
        prompt = build_prompt(
            context,
            question
        )

        return self.llm.generate(prompt)