"""
Interview Preparation Page — generate interview questions from resume.
"""

import streamlit as st

from interview.generator import InterviewGenerator

st.set_page_config(
    page_title="Interview Preparation",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 Interview Preparation")
st.markdown("Generate tailored interview questions based on your resume.")

st.divider()

# Guard — resume must be uploaded first
if not st.session_state.get("resume_ready"):
    st.warning("⚠️ Please upload your resume on the **Resume Analyzer** page first.")
    st.stop()

resume = st.session_state["resume"]

st.info(f"Generating questions for: **{resume.filename}**")

st.divider()

# Controls
st.subheader("⚙️ Configuration")

col1, col2 = st.columns(2)

with col1:
    interview_type = st.selectbox(
        "Interview Type",
        options=["Mixed", "Technical", "HR", "Behavioral"],
        help="Choose the type of questions to generate."
    )

with col2:
    difficulty = st.selectbox(
        "Difficulty Level",
        options=["Easy", "Medium", "Hard"],
        index=1,
        help="Choose the difficulty level of questions."
    )

job_description = st.text_area(
    "Job Description (Optional)",
    height=150,
    placeholder="Paste a job description to generate more targeted questions..."
)

if st.button("Generate Questions", type="primary"):

    with st.spinner("Generating interview questions..."):
        generator = InterviewGenerator()
        report = generator.generate(
            resume=resume,
            interview_type=interview_type.lower(),
            difficulty=difficulty,
            job_description=job_description
        )

    st.session_state["interview_report"] = report

# Show questions if available
if st.session_state.get("interview_report"):

    report = st.session_state["interview_report"]

    st.divider()

    st.subheader("📋 Generated Questions")

    if report.technical_questions:

        with st.expander("💻 Technical Questions", expanded=True):
            for i, q in enumerate(report.technical_questions, 1):
                st.markdown(f"**{i}.** {q}")

    if report.hr_questions:

        with st.expander("🤝 HR Questions", expanded=True):
            for i, q in enumerate(report.hr_questions, 1):
                st.markdown(f"**{i}.** {q}")

    if report.behavioral_questions:

        with st.expander("🧠 Behavioral Questions", expanded=True):
            for i, q in enumerate(report.behavioral_questions, 1):
                st.markdown(f"**{i}.** {q}")

    # Export
    st.divider()

    st.subheader("📥 Export Questions")

    all_questions = []

    if report.technical_questions:
        all_questions.append("TECHNICAL QUESTIONS")
        all_questions.extend(
            f"{i}. {q}"
            for i, q in enumerate(report.technical_questions, 1)
        )
        all_questions.append("")

    if report.hr_questions:
        all_questions.append("HR QUESTIONS")
        all_questions.extend(
            f"{i}. {q}"
            for i, q in enumerate(report.hr_questions, 1)
        )
        all_questions.append("")

    if report.behavioral_questions:
        all_questions.append("BEHAVIORAL QUESTIONS")
        all_questions.extend(
            f"{i}. {q}"
            for i, q in enumerate(report.behavioral_questions, 1)
        )

    st.download_button(
        label="⬇️ Download Questions as TXT",
        data="\n".join(all_questions),
        file_name="interview_questions.txt",
        mime="text/plain"
    )