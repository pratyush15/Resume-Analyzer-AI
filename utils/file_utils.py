
"""
File utilities.
"""

from pathlib import Path
import streamlit as st
from config import UPLOAD_FOLDER, MAX_FILE_SIZE_MB

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def is_allowed_file(filename: str) -> bool:
    """
    Check if the file extension is allowed.
    """
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(uploaded_file) -> str:
    """
    Save uploaded file to the uploads folder.
    Returns the saved file path as string.
    """
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    saved_path = UPLOAD_FOLDER / uploaded_file.name

    with open(saved_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return str(saved_path)


def get_file_size_mb(uploaded_file) -> float:
    """
    Return file size in MB.
    """
    return round(
        uploaded_file.size / (1024 * 1024), 2
    )


def is_within_size_limit(uploaded_file) -> bool:
    """
    Check if file is within the allowed size limit.
    """
    return get_file_size_mb(uploaded_file) <= MAX_FILE_SIZE_MB