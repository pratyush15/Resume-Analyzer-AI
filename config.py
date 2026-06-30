
"""
Application configuration.

Loads all environment variables from the .env file.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# Ollama
OLLAMA_HOST = os.getenv("OLLAMA_BASE_URL")  # renamed to match all imports
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# FAISS
FAISS_INDEX_PATH = BASE_DIR / os.getenv("FAISS_INDEX_PATH")
FAISS_METADATA_PATH = BASE_DIR / os.getenv("FAISS_METADATA_PATH")

# Uploads
UPLOAD_FOLDER = BASE_DIR / os.getenv("UPLOAD_FOLDER")

# Chunking
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))

# Retrieval
TOP_K = int(os.getenv("TOP_K_RESULTS", 5))

# File Upload
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))
SKILLS_FILE = BASE_DIR / "data" / "skills.json"
APP_TITLE = os.getenv("APP_TITLE")