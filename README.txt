health-research-agents
=======================

Multi-agent health research demo using CrewAI-style agents, Streamlit, and Chromadb.

Setup
-----
1. Create and activate a virtualenv:
   python -m venv venv
   venv\Scripts\activate  (Windows)

2. Install dependencies:
   pip install -r requirements.txt

3. Create a .env file based on .env.example and add your OPENAI_API_KEY.

4. (Optional) Preload RAG data:
   python kb/load_data.py

5. Run the Streamlit UI:
   streamlit run ui.py
