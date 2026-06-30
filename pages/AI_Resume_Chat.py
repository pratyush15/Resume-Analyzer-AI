"""
AI Resume Chat Page — RAG-based Q&A on the uploaded resume.
"""

import streamlit as st

from services.chat_service import ChatService

st.set_page_config(
    page_title="AI Resume Chat",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Resume Chat")
st.markdown("Ask anything about your resume. Powered by local LLM via Ollama.")

st.divider()

# Guard — resume must be uploaded first
if not st.session_state.get("resume_ready"):
    st.warning("⚠️ Please upload your resume on the **Resume Analyzer** page first.")
    st.stop()

resume = st.session_state["resume"]

st.info(f"Chatting about: **{resume.filename}**")

st.divider()

# Suggested questions
st.subheader("💡 Suggested Questions")
st.caption("Click any question to ask it instantly.")

suggested_questions = [
    "What are my top technical skills?",
    "Summarize my work experience.",
    "What projects have I worked on?",
    "What is my educational background?",
    "What programming languages do I know?",
    "Do I have any certifications?",
    "What is my most recent job role?",
    "Am I a good fit for a backend developer role?",
]

# Render questions as clickable buttons in a grid
cols = st.columns(2)

for i, question in enumerate(suggested_questions):
    with cols[i % 2]:
        if st.button(question, key=f"suggested_{i}"):
            st.session_state["pending_question"] = question

st.divider()

# Initialize service
chat_service = ChatService()

# Clear history button
col1, col2 = st.columns([6, 1])

with col2:
    if st.button("🗑️ Clear Chat"):
        ChatService.clear_history()
        st.session_state.pop("pending_question", None)
        st.rerun()

# Render chat history
history = ChatService.get_history()

if not history:
    st.markdown(
        "_No messages yet. Click a suggested question or type below._"
    )

for message in history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle suggested question click
if "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

    with st.chat_message("user"):
        st.markdown(question)

    ChatService.add_message("user", question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = chat_service.ask(question)
        st.markdown(answer)

    ChatService.add_message("assistant", answer)

# Chat input
question = st.chat_input("Ask about your resume...")

if question:

    with st.chat_message("user"):
        st.markdown(question)

    ChatService.add_message("user", question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = chat_service.ask(question)
        st.markdown(answer)

    ChatService.add_message("assistant", answer)