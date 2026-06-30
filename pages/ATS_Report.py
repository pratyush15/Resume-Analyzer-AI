
"""
ATS Report Page — 3-part scoring with full UI redesign.
"""

import streamlit as st

from ats.scorer import ATSScorer

st.set_page_config(
    page_title="ATS Report",
    page_icon="📊",
    layout="wide"
)

st.title("📊 ATS Report")
st.markdown("AI-powered resume scoring based on the exact job description you are targeting.")

st.divider()

# Guard
if not st.session_state.get("resume_ready"):
    st.warning("⚠️ Please upload your resume on the **Resume Analyzer** page first.")
    st.stop()

resume = st.session_state["resume"]

st.info(f"Analyzing: **{resume.filename}**")

st.divider()

# Mandatory JD input
st.subheader("📋 Job Description")
st.caption(
    "Required — ATS scoring is driven entirely by the job description. "
    "Hard skills, semantic profile, and experience requirements are all extracted from it."
)

jd_text = st.text_area(
    "Paste the job description here",
    height=220,
    placeholder="e.g. We are looking for a Python developer with 3+ years of experience in FastAPI, LangChain, Docker..."
)

jd_provided = bool(jd_text and jd_text.strip())

if not jd_provided:
    st.warning("⚠️ Paste a job description above to enable ATS analysis.")

if st.button("Run ATS Analysis", type="primary", disabled=not jd_provided):

    with st.spinner("Running 3-part ATS analysis..."):
        scorer = ATSScorer()
        report = scorer.analyze(resume, jd_text)

    st.session_state["ats_report"] = report
    st.session_state["ats_jd_text"] = jd_text
    st.toast("✅ ATS analysis complete!", icon="📊")

if not st.session_state.get("ats_report"):
    st.stop()

report = st.session_state["ats_report"]
jd_text = st.session_state.get("ats_jd_text", "")

st.divider()

# -----------------------------------------------------------------------
# HERO SECTION — Overall Score
# -----------------------------------------------------------------------

score = report.overall_score

if score >= 80:
    color = "#22c55e"
    tier = "Strong Match ✅"
    tier_color = "green"
elif score >= 60:
    color = "#f59e0b"
    tier = "Needs Optimization ⚠️"
    tier_color = "orange"
else:
    color = "#ef4444"
    tier = "Low Match ❌"
    tier_color = "red"

st.subheader("🎯 Overall ATS Match Score")

col1, col2 = st.columns([1, 2])

with col1:

    # Circular progress using HTML
    st.markdown(
        f"""
        <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; padding: 20px;">
            <svg width="180" height="180" viewBox="0 0 180 180">
                <circle cx="90" cy="90" r="80" fill="none" stroke="#e5e7eb" stroke-width="16"/>
                <circle cx="90" cy="90" r="80" fill="none"
                    stroke="{color}"
                    stroke-width="16"
                    stroke-dasharray="{2 * 3.14159 * 80}"
                    stroke-dashoffset="{2 * 3.14159 * 80 * (1 - score / 100)}"
                    stroke-linecap="round"
                    transform="rotate(-90 90 90)"/>
                <text x="90" y="85" text-anchor="middle"
                    font-size="32" font-weight="bold" fill="{color}">{score}%</text>
                <text x="90" y="112" text-anchor="middle"
                    font-size="13" fill="#6b7280">ATS Score</text>
            </svg>
            <div style="margin-top:8px; font-size:18px; font-weight:600; color:{color};">
                {tier}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown("#### 📈 Score Breakdown")

    # Hard Skills
    st.markdown(f"**💻 Hard Skills Match** — {report.hard_skills_score:.1f}%")
    stars = "⭐" * int(report.hard_skills_score // 20) + "✩" * (5 - int(report.hard_skills_score // 20))
    st.markdown(f"{stars} *(40% of final score)*")
    st.progress(min(report.hard_skills_score / 100, 1.0))

    st.markdown("")

    # Semantic
    st.markdown(f"**🧠 Semantic Profile Match** — {report.semantic_score:.1f}%")
    stars = "⭐" * int(report.semantic_score // 20) + "✩" * (5 - int(report.semantic_score // 20))
    st.markdown(f"{stars} *(40% of final score)*")
    st.progress(min(report.semantic_score / 100, 1.0))

    st.markdown("")

    # Experience & Education
    st.markdown(f"**🎓 Experience & Education** — {report.exp_edu_score:.1f}%")
    stars = "⭐" * int(report.exp_edu_score // 20) + "✩" * (5 - int(report.exp_edu_score // 20))
    st.markdown(f"{stars} *(20% of final score)*")
    st.progress(min(report.exp_edu_score / 100, 1.0))

st.divider()

# -----------------------------------------------------------------------
# KEYWORD GAP ANALYSIS
# -----------------------------------------------------------------------

st.subheader("🔍 Keyword Gap Analysis")
st.caption("Keywords extracted directly from the job description.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**✅ Matched Keywords**")
    if report.keyword_report.matched_skills:
        tags_html = " ".join([
            f'<span style="background:#dcfce7; color:#166534; padding:4px 10px; '
            f'border-radius:12px; margin:3px; display:inline-block; '
            f'font-size:13px; font-weight:500;">{skill}</span>'
            for skill in report.keyword_report.matched_skills
        ])
        st.markdown(tags_html, unsafe_allow_html=True)
    else:
        st.write("No matched keywords found.")

with col2:
    st.markdown("**❌ Missing Keywords**")
    if report.keyword_report.missing_skills:
        tags_html = " ".join([
            f'<span style="background:#fee2e2; color:#991b1b; padding:4px 10px; '
            f'border-radius:12px; margin:3px; display:inline-block; '
            f'font-size:13px; font-weight:500;">{skill}</span>'
            for skill in report.keyword_report.missing_skills
        ])
        st.markdown(tags_html, unsafe_allow_html=True)
    else:
        st.success("All keywords matched!")

st.divider()

# -----------------------------------------------------------------------
# SECTION BREAKDOWN
# -----------------------------------------------------------------------

st.subheader("📂 Section Detection")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**✅ Detected Sections**")
    if report.detected_sections:
        for section in report.detected_sections:
            st.markdown(f"✔ {section}")
    else:
        st.write("None detected.")

with col2:
    st.markdown("**❌ Missing Sections**")
    if report.missing_sections:
        for section in report.missing_sections:
            st.markdown(
                f'<span style="color:#ef4444;">✖ {section}</span>',
                unsafe_allow_html=True
            )
    else:
        st.success("All sections present!")

st.divider()

# -----------------------------------------------------------------------
# GRAMMAR
# -----------------------------------------------------------------------

st.subheader("📝 Grammar Check")

grammar = report.grammar_report

col1, col2 = st.columns([1, 3])

with col1:
    if grammar.total_errors == 0:
        st.success("✅ Pass")
        st.caption("No grammar issues found.")
    elif grammar.total_errors <= 5:
        st.warning("⚠️ Minor Issues")
        st.caption(f"{grammar.total_errors} issues found.")
    else:
        st.error("❌ Needs Attention")
        st.caption(f"{grammar.total_errors} issues found.")

with col2:
    if grammar.suggestions:
        with st.expander("View Grammar Issues"):
            for issue in grammar.suggestions:
                st.markdown(
                    f"- **Issue:** `{issue['incorrect']}` → "
                    f"**Fix:** `{issue['replacement']}` "
                    f"({issue['message']})"
                )

st.divider()

# -----------------------------------------------------------------------
# AI SUGGESTIONS
# -----------------------------------------------------------------------

st.subheader("💡 AI-Powered Suggestions")
st.caption("Specific actions to improve your ATS score for this role.")

if report.suggestions:
    for i, suggestion in enumerate(report.suggestions, 1):
        st.markdown(
            f"""
            <div style="background:#f8fafc; border-left:4px solid #3b82f6;
                padding:12px 16px; margin:8px 0; border-radius:4px;
                font-size:14px; color:#1e293b;">
                <strong>{i}.</strong> {suggestion}
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.success("🎉 Your resume is an excellent match for this role!")