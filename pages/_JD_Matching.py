"""
JD Matching Page — compare resume against a job description.
"""

import streamlit as st

from jd_matching.matcher import JDMatcher

st.set_page_config(
    page_title="JD Matching",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 JD Matching")
st.markdown("Paste a job description to see how well your resume matches it.")

st.divider()

# Guard — resume must be uploaded first
if not st.session_state.get("resume_ready"):
    st.warning("⚠️ Please upload your resume on the **Resume Analyzer** page first.")
    st.stop()

resume = st.session_state["resume"]

st.info(f"Comparing against: **{resume.filename}**")

st.subheader("📋 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=250,
    placeholder="e.g. We are looking for a Python developer with experience in FastAPI, LangChain..."
)

if st.button("Analyze Match", type="primary"):

    if not job_description.strip():
        st.warning("Please paste a job description before analyzing.")
        st.stop()

    with st.spinner("Comparing resume against job description..."):
        matcher = JDMatcher()
        report = matcher.analyze(resume, job_description)

    st.session_state["jd_report"] = report

# Show report if available
if st.session_state.get("jd_report"):

    report = st.session_state["jd_report"]

    st.divider()

    # Overall match
    st.subheader("🎯 Overall Match Score")

    score = report.overall_match

    if score >= 75:
        st.success(f"### {score}% — Strong Match ✅")
    elif score >= 50:
        st.warning(f"### {score}% — Partial Match ⚠️")
    else:
        st.error(f"### {score}% — Weak Match ❌")

    st.divider()

    # Score breakdown
    st.subheader("📈 Score Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Semantic Similarity",
            f"{report.semantic_similarity}%",
            help="How closely your resume text matches the JD in meaning."
        )

    with col2:
        skill_match = (
            round(len(report.matched_skills) /
            (len(report.matched_skills) + len(report.missing_skills)) * 100, 2)
            if (report.matched_skills or report.missing_skills) else 0
        )
        st.metric(
            "Skill Match",
            f"{skill_match}%",
            help="Percentage of JD skills found in your resume."
        )

    st.divider()

    # Skills breakdown
    st.subheader("💻 Skills Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**✅ Matched Skills**")
        if report.matched_skills:
            for skill in report.matched_skills:
                st.write(f"✔ {skill}")
        else:
            st.write("No matching skills found.")

    with col2:
        st.markdown("**❌ Missing Skills**")
        if report.missing_skills:
            for skill in report.missing_skills:
                st.write(f"✖ {skill}")
        else:
            st.success("Your resume covers all required skills!")

    st.divider()

    # Recommendations
    st.subheader("💡 Recommendations")

    if report.recommendations:
        for rec in report.recommendations:
            st.write(f"• {rec}")
    else:
        st.success("Great fit! No major gaps found.")