"""
AI Resume Analyzer — Home Page
"""

import streamlit as st

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# --- Header ---
st.title("📄 AI Resume Analyzer")
st.markdown(
    "A fully local, zero-cost AI-powered resume analysis tool. "
    "Built with FastAPI, LangChain, Ollama, FAISS, and Streamlit."
)

st.divider()

# --- Status Banner ---
st.subheader("📊 Session Status")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.session_state.get("resume_ready"):
        st.success("✅ Resume Loaded")
        st.caption(st.session_state["resume"].filename)
    else:
        st.warning("⚠️ No Resume Loaded")
        st.caption("Go to Resume Analyzer")

with col2:
    if "ats_report" in st.session_state:
        st.success("✅ ATS Report Ready")
        st.caption(
            f"Score: {st.session_state['ats_report'].overall_score}%"
        )
    else:
        st.info("📊 ATS Report")
        st.caption("Not generated yet")

with col3:
    if "jd_report" in st.session_state:
        st.success("✅ JD Match Ready")
        st.caption(
            f"Match: {st.session_state['jd_report'].overall_match}%"
        )
    else:
        st.info("🎯 JD Match")
        st.caption("Not generated yet")

with col4:
    if "interview_report" in st.session_state:
        st.success("✅ Questions Ready")
        st.caption("Interview prep done")
    else:
        st.info("🎤 Interview Prep")
        st.caption("Not generated yet")

st.divider()

# --- Feature Cards ---
st.subheader("🚀 Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📄 Resume Analyzer")
    st.markdown(
        "Upload your PDF or DOCX resume. "
        "Extracts contact info, skills, and all sections automatically."
    )

    st.markdown("### 📊 ATS Report")
    st.markdown(
        "Score your resume against ATS criteria — "
        "keyword match, grammar, length, and section detection."
    )

with col2:
    st.markdown("### 🎯 JD Matching")
    st.markdown(
        "Paste any job description and get a match score, "
        "skill gap analysis, and recommendations."
    )

    st.markdown("### 🤖 AI Resume Chat")
    st.markdown(
        "Ask anything about your resume using a local RAG pipeline. "
        "Powered by Ollama — fully offline."
    )

with col3:
    st.markdown("### 🎤 Interview Preparation")
    st.markdown(
        "Generate technical, HR, and behavioral interview questions "
        "tailored to your resume and difficulty level."
    )
    
    st.markdown("### ✉️ Cover Letter Generator")
    st.markdown(
        "Generate a tailored, ATS-friendly cover letter "
        "for any role using your resume and the job description."
    )

    st.markdown("### ⚙️ Settings")
    st.markdown(
        "Check Ollama connection, switch models, "
        "inspect session state, and reset anytime."
    )

st.divider()

# --- Quick Start Guide ---
st.subheader("⚡ Quick Start")

st.markdown("""
1. Make sure **Ollama** is running locally with your models pulled:
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

2. Open **Resume Analyzer** from the sidebar and upload your resume.

3. Navigate to any feature page — all pages read from the uploaded resume automatically.
""")

st.divider()

# --- Tech Stack ---
st.subheader("🛠️ Tech Stack")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Backend**
    - Python
    """)

with col2:
    st.markdown("""
    **AI / ML**
    - Ollama (Mistral, nomic-embed-text)
    - FAISS
    - scikit-learn
    """)

with col3:
    st.markdown("""
    **Frontend**
    - Streamlit
    - Multi-page architecture
    """)

st.divider()

st.caption(
    "Built by Pratyush · Fully local · Zero API costs · "
    "Open source stack"
)