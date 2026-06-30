"""
Cover Letter Generator — generates tailored cover letters 
"""

import streamlit as st

from embeddings.embedder import Embedder
from embeddings.faiss_db import FAISSVectorDB
from llm.ollama_client import OllamaClient
from llm.prompts import build_cover_letter_prompt

st.set_page_config(
    page_title="Cover Letter Generator",
    page_icon="✉️",
    layout="wide"
)

st.title("✉️ Cover Letter Generator")
st.markdown(
    "Generate a tailored, ATS-friendly cover letter "
    "based on your resume and the role you are applying for."
)

st.divider()

# Guard
if not st.session_state.get("resume_ready"):
    st.warning(
        "⚠️ Please upload your resume on the "
        "**Resume Analyzer** page first."
    )
    st.stop()

resume = st.session_state["resume"]

st.info(f"Generating cover letter for: **{resume.filename}**")

st.divider()

# Inputs
st.subheader("🎯 Job Details")

col1, col2 = st.columns(2)

with col1:
    job_title = st.text_input(
        "Job Title",
        placeholder="e.g. AI Engineer, Backend Developer..."
    )

with col2:
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g. Anthropic, Google, Zepto..."
    )

jd_text = st.text_area(
    "Job Description (Recommended)",
    height=180,
    placeholder=(
        "Paste the job description here for a more targeted cover letter. "
        "Leave empty to generate a general one based on your resume."
    )
)

st.divider()

# Tone selector
st.subheader("🎨 Tone")

tone = st.radio(
    "Select cover letter tone",
    options=["Professional", "Enthusiastic", "Concise"],
    horizontal=True,
    help=(
        "Professional — formal and structured. "
        "Enthusiastic — warm and energetic. "
        "Concise — short and to the point."
    )
)

# Validate inputs
inputs_valid = bool(
    job_title and job_title.strip() and
    company_name and company_name.strip()
)

if not inputs_valid:
    st.warning("⚠️ Please enter both Job Title and Company Name.")

if st.button(
    "Generate Cover Letter",
    type="primary",
    disabled=not inputs_valid
):

    with st.spinner("Retrieving resume context and generating cover letter..."):

        try:
            # Retrieve relevant resume chunks via FAISS
            embedder = Embedder()
            db = FAISSVectorDB()
            db.load()

            # Build query from job title + company + JD snippet
            query = f"{job_title} {company_name} {jd_text[:300]}"
            query_embedding = embedder.embed(query)

            chunks = db.search(query_embedding, top_k=8)
            context = "\n\n".join(chunk.text for chunk in chunks)

            # Build prompt with tone instruction
            tone_instruction = {
                "Professional": "Use a formal, structured, and professional tone.",
                "Enthusiastic": "Use a warm, energetic, and enthusiastic tone.",
                "Concise": "Keep it brief and to the point — no more than 3 short paragraphs."
            }[tone]

            prompt = build_cover_letter_prompt(
                context=context,
                job_title=job_title,
                company_name=company_name,
                jd_text=jd_text
            )

            # Append tone instruction to prompt
            prompt += f"\n\nTone instruction: {tone_instruction}"

            llm = OllamaClient()
            cover_letter = llm.generate(prompt)

            st.session_state["cover_letter"] = cover_letter
            st.session_state["cover_letter_meta"] = {
                "job_title": job_title,
                "company_name": company_name,
                "tone": tone
            }

            st.toast("✅ Cover letter generated!", icon="✉️")

        except Exception as e:
            st.error(f"Error generating cover letter: {e}")
            st.stop()

# Show cover letter if available
if st.session_state.get("cover_letter"):

    cover_letter = st.session_state["cover_letter"]
    meta = st.session_state.get("cover_letter_meta", {})

    st.divider()

    st.subheader(
        f"✉️ Cover Letter — "
        f"{meta.get('job_title', '')} at "
        f"{meta.get('company_name', '')}"
    )
    st.caption(f"Tone: {meta.get('tone', 'Professional')}")

    # Editable text area so user can tweak before copying
    edited_letter = st.text_area(
        "Edit your cover letter below before copying or downloading",
        value=cover_letter,
        height=500
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        # Download as TXT
        st.download_button(
            label="⬇️ Download as TXT",
            data=edited_letter,
            file_name=f"cover_letter_{meta.get('company_name', 'company').replace(' ', '_')}.txt",
            mime="text/plain"
        )

    with col2:
        # Regenerate button
        if st.button("🔄 Regenerate", type="secondary"):
            del st.session_state["cover_letter"]
            del st.session_state["cover_letter_meta"]
            st.rerun()