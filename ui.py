import streamlit as st
from controller import SystemController

# Initialize controller
if 'controller' not in st.session_state:
    st.session_state.controller = SystemController()
    st.session_state.controller.initialize_system()

if 'session_id' not in st.session_state:
    st.session_state.session_id = st.session_state.controller.session_manager.create_session()

if 'last_response' not in st.session_state:
    st.session_state.last_response = None

controller = st.session_state.controller

st.set_page_config(page_title="Health Research Agentic System", layout="wide")

st.title("COMP248_Project - Health Research Agentic System" "🩺🤖")
st.write(
    "This demo uses a multi-agent design (Planner, Search, Summarizer, Reflective) "
    "to help a Research Analyst explore health-related questions.\n\n"
    "**Note:** This is for educational purposes only and does *not* provide medical advice."
)

# Query Section
st.header("What health topic would you like to research?")
query = st.text_input("Enter your health-related enquiry:", key="query_input")

if st.button("Ask your question", key="run_button"):
    if query:
        with st.spinner("Agents are working on your request..."):
            response = controller.handle_query(query, st.session_state.session_id)
        
        st.session_state.last_response = response
        
        st.subheader("Result")
        
        if response.is_successful():
            st.success(f"Query processed successfully in {response.execution_time:.2f}s")
            
            # Display agent logs (which contain the actual output for now)
            if response.agent_logs:
                for log in response.agent_logs:
                    st.markdown(log)
            else:
                st.warning("No response content available")
        else:
            st.error(f"Error: {response.error_message}")
    else:
        st.warning("Please enter a query first.")

# Feedback Section
if st.session_state.last_response and st.session_state.last_response.is_successful():
    st.markdown("---")
    st.header("📝 Provide Feedback")
    st.write("Help us improve the summary quality by providing your feedback:")
    
    with st.form("feedback_form"):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            rating = st.slider("Rate this summary:", 1, 5, 3, key="rating_slider")
            improvement = st.checkbox("Request improved summary", key="improvement_check")
        
        with col2:
            comments = st.text_area(
                "Comments or suggestions (optional):",
                placeholder="What could be improved? What information is missing?",
                key="comments_area"
            )
        
        submitted = st.form_submit_button("Submit Feedback")
        
        if submitted:
            with st.spinner("Processing your feedback..."):
                feedback_response = controller.handle_feedback(
                    summary_id=st.session_state.last_response.response_id,
                    rating=rating,
                    comments=comments,
                    improvement_requested=improvement,
                    session_id=st.session_state.session_id
                )
            
            if feedback_response.is_successful():
                st.success("Thank you for your feedback!")
                
                # Display feedback acknowledgment
                for log in feedback_response.agent_logs:
                    st.info(log)
                
                if improvement:
                    st.info("🔄 Your request for an improved summary has been noted. "
                           "This feature will trigger re-summarization in the full implementation.")
            else:
                st.error(f"Error processing feedback: {feedback_response.error_message}")

# Session History (Optional)
with st.expander("📊 Session History"):
    history = controller.get_session_state(st.session_state.session_id)
    if history:
        st.write(f"**Session ID:** {history['session_id']}")
        st.write(f"**Queries submitted:** {len(history['queries'])}")
        st.write(f"**Feedback provided:** {len(history['feedback'])}")
        
        if history['queries']:
            st.subheader("Query History")
            for i, q in enumerate(history['queries'], 1):
                st.text(f"{i}. {q['text']}")
    else:
        st.write("No session history available.")
