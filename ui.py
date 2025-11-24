import streamlit as st
from app import run_system

st.set_page_config(page_title="Health Research Agentic System", layout="wide")

st.title("🧠 Health Research Agentic System")
st.write(
    "This demo uses a multi-agent design (Planner, Search, Summarizer, Reflective) "
    "to help a Research Analyst explore health-related questions.\n\n"
    "**Note:** This is for educational purposes only and does *not* provide medical advice."
)

query = st.text_input("Enter your health-related enquiry:")

if st.button("Run Multi-Agent Pipeline"):
    with st.spinner("Agents are working on your request..."):
        result = run_system(query)
    st.subheader("Result")
    st.write(result)
