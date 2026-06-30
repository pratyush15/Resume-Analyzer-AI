"""
Settings Page — configure Ollama models and app preferences.
"""

import streamlit as st
import ollama

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Settings")
st.markdown("Configure your local Ollama models and app preferences.")

st.divider()

# --- Ollama Connection Status ---
st.subheader("🔌 Ollama Connection")

try:
    client = ollama.Client(host=st.session_state.get("ollama_host", "http://localhost:11434"))
    models_response = client.list()
    available_models = [m.model for m in models_response.models]
    st.success(f"✅ Connected to Ollama. {len(available_models)} model(s) found.")

except Exception:
    available_models = []
    st.error("❌ Could not connect to Ollama. Make sure it is running locally.")

st.divider()

# --- Model Configuration ---
st.subheader("🤖 Model Configuration")

from config import LLM_MODEL, EMBEDDING_MODEL

col1, col2 = st.columns(2)

with col1:
    st.markdown("**LLM Model**")
    st.caption("Used for chat, interview questions, and JD analysis.")

    if available_models:
        llm_model = st.selectbox(
            "Select LLM Model",
            options=available_models,
            index=(
                available_models.index(LLM_MODEL)
                if LLM_MODEL in available_models
                else 0
            )
        )
    else:
        llm_model = st.text_input(
            "LLM Model Name",
            value=LLM_MODEL or "mistral"
        )

with col2:
    st.markdown("**Embedding Model**")
    st.caption("Used for FAISS indexing and semantic search.")

    if available_models:
        embedding_model = st.selectbox(
            "Select Embedding Model",
            options=available_models,
            index=(
                available_models.index(EMBEDDING_MODEL)
                if EMBEDDING_MODEL in available_models
                else 0
            )
        )
    else:
        embedding_model = st.text_input(
            "Embedding Model Name",
            value=EMBEDDING_MODEL or "nomic-embed-text"
        )

st.divider()

# --- Session State Inspector ---
st.subheader("🧠 Current Session State")

col1, col2, col3 = st.columns(3)

with col1:
    resume_ready = st.session_state.get("resume_ready", False)
    if resume_ready:
        st.success("✅ Resume Loaded")
        st.caption(st.session_state["resume"].filename)
    else:
        st.warning("⚠️ No Resume Loaded")

with col2:
    ats_ready = "ats_report" in st.session_state
    if ats_ready:
        st.success("✅ ATS Report Ready")
        st.caption(f"Score: {st.session_state['ats_report'].overall_score}%")
    else:
        st.warning("⚠️ No ATS Report")

with col3:
    jd_ready = "jd_report" in st.session_state
    if jd_ready:
        st.success("✅ JD Report Ready")
        st.caption(f"Match: {st.session_state['jd_report'].overall_match}%")
    else:
        st.warning("⚠️ No JD Report")

st.divider()

# --- Clear Session ---
st.subheader("🗑️ Reset Session")

st.markdown("Clear all loaded data and start fresh.")

if st.button("Clear All Session Data", type="secondary"):
    for key in [
        "resume",
        "resume_ready",
        "ats_report",
        "jd_report",
        "interview_report",
        "chat_history"
    ]:
        st.session_state.pop(key, None)

    st.success("✅ Session cleared. Go to Resume Analyzer to upload a new resume.")
    st.rerun()