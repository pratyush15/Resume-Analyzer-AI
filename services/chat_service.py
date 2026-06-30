"""
Chat Service — handles RAG-based resume Q&A.
"""

import streamlit as st

from embeddings.embedder import Embedder
from embeddings.faiss_db import FAISSVectorDB
from llm.ollama_client import OllamaClient
from llm.prompts import build_prompt


class ChatService:

    def __init__(self):
        self.embedder = Embedder()
        self.db = FAISSVectorDB()
        self.db.load()
        self.llm = OllamaClient()

    def ask(self, question: str) -> str:
        """
        Embed the question, retrieve relevant chunks,
        build prompt, and return LLM answer.
        """

        embedding = self.embedder.embed(question)

        chunks = self.db.search(embedding)

        context = "\n\n".join(
            chunk.text for chunk in chunks
        )

        prompt = build_prompt(context, question)

        return self.llm.generate(prompt)

    @staticmethod
    def get_history() -> list:
        """
        Return chat history from session state.
        """
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        return st.session_state["chat_history"]

    @staticmethod
    def add_message(role: str, content: str):
        """
        Append a message to chat history.
        """
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        st.session_state["chat_history"].append({
            "role": role,
            "content": content
        })

    @staticmethod
    def clear_history():
        """
        Clear chat history.
        """
        st.session_state["chat_history"] = []