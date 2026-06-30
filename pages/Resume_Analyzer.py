"""
Resume Analyzer Page — upload and parse resume.
"""

import streamlit as st

from services.resume_service import ResumeService
from utils.file_utils import is_allowed_file

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Resume Analyzer")
st.markdown("Upload your resume to get started. All other pages depend on this step.")

st.divider()

uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

if uploaded_file:

    if not is_allowed_file(uploaded_file.name):
        st.error("Unsupported file type. Please upload a PDF or DOCX.")
        st.stop()

    with st.spinner("Parsing and indexing your resume..."):
        success = ResumeService.process(uploaded_file)

    if success:
        st.success("✅ Resume processed successfully!")

    resume = st.session_state["resume"]

    st.divider()

    # Contact Info
    st.subheader("👤 Contact Information")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"📧 **Email:** {resume.email or 'Not found'}")
        st.write(f"📞 **Phone:** {resume.phone or 'Not found'}")

    with col2:
        st.write(f"🔗 **LinkedIn:** {resume.linkedin or 'Not found'}")
        st.write(f"🐙 **GitHub:** {resume.github or 'Not found'}")

    st.divider()

    # Skills
    st.subheader("💻 Detected Skills")

    if resume.skills:
        st.write(", ".join(resume.skills))
    else:
        st.warning("No skills detected.")

    st.divider()

    # Resume sections
    st.subheader("📋 Resume Sections")

    tabs = st.tabs([
        "Summary",
        "Experience",
        "Education",
        "Projects",
        "Certifications",
        "Full Text"
    ])

    with tabs[0]:
        st.write(resume.summary or "Not found.")

    with tabs[1]:
        st.write(resume.experience or "Not found.")

    with tabs[2]:
        st.write(resume.education or "Not found.")

    with tabs[3]:
        st.write(resume.projects or "Not found.")

    with tabs[4]:
        st.write(resume.certifications or "Not found.")

    with tabs[5]:
        st.text(resume.cleaned_text)

else:

    # Show info if no resume uploaded yet
    if st.session_state.get("resume_ready"):
        st.info(
            f"✅ Resume already loaded: "
            f"**{st.session_state['resume'].filename}**. "
            f"Upload a new one to replace it."
        )
    else:
        st.info("👆 Upload a resume above to begin.")