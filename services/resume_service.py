"""
Resume Service — handles parsing, embedding, and session caching.
"""

from pathlib import Path
import streamlit as st
from parser.pdf_parser import PDFParser
from parser.doc_parser import DOCParser
from parser.text_cleaner import TextCleaner
from parser.resume_extractor import ResumeExtractor
from embeddings.chunker import TextChunker
from embeddings.embedder import Embedder
from embeddings.faiss_db import FAISSVectorDB
from models.document_chunk import DocumentChunk


class ResumeService:

    @staticmethod
    def process(uploaded_file) -> bool:
        """
        Parse, embed, and index the uploaded resume.
        Stores result in st.session_state.
        Returns True if successful.
        """

        suffix = Path(uploaded_file.name).suffix.lower()

        # Save to a temp path
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        saved_path = upload_dir / uploaded_file.name

        with open(saved_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Parse
        if suffix == ".pdf":
            raw_text = PDFParser.extract_text(str(saved_path))
        else:
            raw_text = DOCParser.extract_text(str(saved_path))

        cleaned_text = TextCleaner.clean(raw_text)

        # Extract structured resume
        extractor = ResumeExtractor()
        resume = extractor.build(
            filename=uploaded_file.name,
            raw_text=raw_text,
            cleaned_text=cleaned_text
        )

        # Chunk + embed + index
        chunks = TextChunker.chunk(cleaned_text)

        embedder = Embedder()
        embeddings = [embedder.embed(chunk) for chunk in chunks]

        doc_chunks = [
            DocumentChunk(chunk_id=i, text=chunk, source=uploaded_file.name)
            for i, chunk in enumerate(chunks)
        ]

        db = FAISSVectorDB()
        db.create_index(dimension=len(embeddings[0]))
        db.add_documents(embeddings, doc_chunks)
        db.save()

        # Store in session
        st.session_state["resume"] = resume
        st.session_state["resume_ready"] = True

        return True