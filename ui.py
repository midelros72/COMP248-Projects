import streamlit as st
from controller import SystemController
import time

# --- Configuration & Setup ---
st.set_page_config(
    page_title="Health Research Agentic System",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for "Slick & Professional" Look ---
st.markdown("""
<style>
    /* Main Background & Font */
    .stApp {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
    }
    
    /* Card Container Styling */
    .card {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #e9ecef;
    }
    
    /* Result Section Styling */
    .result-header {
        color: #2980b9;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    
    /* Feedback Section Styling */
    .feedback-container {
        background-color: #f0f7fb;
        border-left: 5px solid #3498db;
        padding: 1.5rem;
        border-radius: 5px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #2c3e50;
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ecf0f1 !important;
    }
    
    /* Button Styling */
    .stButton>button {
        border-radius: 5px;
        font-weight: 600;
    }
    
    /* Status Message Styling */
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        color: #155724;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin-bottom: 1rem;
    }
    
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialization ---
if 'controller' not in st.session_state:
    st.session_state.controller = SystemController()
    st.session_state.controller.initialize_system()

if 'session_id' not in st.session_state:
    st.session_state.session_id = st.session_state.controller.session_manager.create_session()

if 'last_response' not in st.session_state:
    st.session_state.last_response = None

controller = st.session_state.controller

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/heart-with-pulse.png", width=64)
    st.title("Research Hub")
    st.markdown("---")
    
    st.subheader("About")
    st.info(
        "This system utilizes a multi-agent architecture (Planner, Search, Summarizer, Reflective) "
        "to conduct comprehensive health research."
    )
    
    st.markdown("### 📊 Session Stats")
    history = controller.get_session_state(st.session_state.session_id)
    if history:
        st.metric("Queries", len(history['queries']))
        st.metric("Feedback Given", len(history['feedback']))
    
    st.markdown("---")
    if st.button("New Session", type="secondary"):
        st.session_state.session_id = st.session_state.controller.session_manager.create_session()
        st.session_state.last_response = None
        st.rerun()

# --- Main Content ---
st.markdown('<div class="main-header">Health Research Agentic System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Intelligent analysis powered by multi-agent collaboration.</div>', unsafe_allow_html=True)

# Disclaimer
st.warning("⚠️ **Disclaimer:** This tool is for educational purposes only and does not provide medical advice. Always consult a healthcare professional.")

# Search Section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🔍 Start Your Research")
query = st.text_input("Enter a health topic or question:", placeholder="e.g., What are the benefits of Vitamin D?", key="query_input")

col1, col2 = st.columns([1, 5])
with col1:
    search_button = st.button("Analyze Topic", type="primary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if search_button:
    if query:
        # Progress Indicator
        with st.status("🚀 Agents are collaborating...", expanded=True) as status:
            st.write("📋 **Planner Agent:** Breaking down the query...")
            time.sleep(0.5) # UI smoothing
            st.write("🔎 **Search Agent:** Retrieving relevant medical data...")
            time.sleep(0.5)
            st.write("📝 **Summarizer Agent:** Synthesizing information...")
            time.sleep(0.5)
            st.write("🤔 **Reflective Agent:** Reviewing for accuracy and safety...")
            
            response = controller.handle_query(query, st.session_state.session_id)
            st.session_state.last_response = response
            
            if response.is_successful():
                status.update(label="✅ Research Complete!", state="complete", expanded=False)
            else:
                status.update(label="❌ Process Failed", state="error", expanded=True)

    else:
        st.warning("Please enter a query first.")

# Results Display
if st.session_state.last_response:
    response = st.session_state.last_response
    
    if response.is_successful():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="result-header">📋 Research Report</div>', unsafe_allow_html=True)
        
        # Display the main result
        # Assuming the last log or a specific part of the response contains the final summary
        # Ideally, the controller should return the structured summary separately.
        # For now, we display the logs which contain the output.
        
        if response.agent_logs:
            # Try to find the final summary in the logs if possible, or display all nicely
            # For this demo, we'll display the last log entry as it usually contains the final result in the fallback mode
            # In a real app, we'd parse this better.
            
            # Displaying all logs in a clean format
            for log in response.agent_logs:
                # Clean up log formatting if needed
                st.markdown(log)
        else:
            st.info("No detailed content available.")
            
        st.markdown(f"*Processing Time: {response.execution_time:.2f}s*", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Feedback Section
        st.markdown('<div class="card feedback-container">', unsafe_allow_html=True)
        st.subheader("📝 Quality Assurance Feedback")
        
        with st.form("feedback_form"):
            f_col1, f_col2 = st.columns([1, 2])
            
            with f_col1:
                rating = st.slider("Rate the quality of this report:", 1, 5, 3)
                improvement = st.checkbox("Request detailed refinement")
            
            with f_col2:
                comments = st.text_area("Reviewer Notes:", placeholder="Any missing information or inaccuracies?")
            
            submitted = st.form_submit_button("Submit Review")
            
            if submitted:
                with st.spinner("Processing feedback..."):
                    feedback_response = controller.handle_feedback(
                        summary_id=response.response_id,
                        rating=rating,
                        comments=comments,
                        improvement_requested=improvement,
                        session_id=st.session_state.session_id
                    )
                
                if feedback_response.is_successful():
                    st.success("✅ Feedback recorded successfully.")
                    if improvement:
                        st.info("🔄 Refinement request queued.")
                else:
                    st.error(f"❌ Error recording feedback: {feedback_response.error_message}")
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown(f'<div class="error-box">Error: {response.error_message}</div>', unsafe_allow_html=True)

# Session History Expander (kept at bottom for reference)
with st.expander("📜 View Session History"):
    if history and history['queries']:
        for i, q in enumerate(reversed(history['queries']), 1):
            st.markdown(f"**{i}.** {q['text']} ({q['timestamp']})")
    else:
        st.write("No history yet.")
