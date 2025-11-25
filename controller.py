"""
System Controller

Main controller that mediates between UI and backend agents.
Handles input validation, session management, and response formatting.
"""
from typing import Optional
import uuid
import time

from models import Query, QueryResponse, UserFeedback, QueryStatus
from validator import InputValidator
from session_manager import SessionManager
from app import run_system


class SystemController:
    """Controller layer between UI and agents."""
    
    def __init__(self):
        """Initialize the system controller."""
        self.validator = InputValidator()
        self.session_manager = SessionManager()
        self.initialized = False
    
    def initialize_system(self) -> None:
        """Initialize the system and verify all components."""
        try:
            # Add any initialization logic here
            # For now, just mark as initialized
            self.initialized = True
            print("System controller initialized successfully")
        except Exception as e:
            print(f"System initialization failed: {e}")
            raise
    
    def handle_query(self, query_text: str, session_id: Optional[str] = None) -> QueryResponse:
        """
        Handle a user query.
        
        Args:
            query_text: The user's query text
            session_id: Optional session ID for tracking
            
        Returns:
            QueryResponse with results or error
        """
        start_time = time.time()
        
        # Create or get session
        if not session_id:
            session_id = self.session_manager.create_session()
        
        # Generate query ID
        query_id = str(uuid.uuid4())
        response_id = str(uuid.uuid4())
        
        # Validate input
        if not self.validator.validate_query(query_text):
            query = Query(
                query_id=query_id,
                text=query_text,
                session_id=session_id
            )
            return QueryResponse(
                response_id=response_id,
                query=query,
                status=QueryStatus.FAILED.value,
                error_message="Invalid query. Please check length and content.",
                execution_time=time.time() - start_time
            )
        
        # Sanitize input
        sanitized_query = self.validator.sanitize_input(query_text)
        
        # Create Query object
        query = Query(
            query_id=query_id,
            text=sanitized_query,
            session_id=session_id
        )
        
        # Update session
        self.session_manager.update_session(session_id, query=query)
        
        try:
            # Process query through agent system
            result = run_system(sanitized_query)
            
            # Create response (simplified for now - will be enhanced with proper Summary/Reflection objects)
            response = QueryResponse(
                response_id=response_id,
                query=query,
                status=QueryStatus.COMPLETED.value,
                execution_time=time.time() - start_time
            )
            
            # Extract text from CrewAI result object
            if hasattr(result, 'raw'):
                # CrewAI result object
                result_text = str(result.raw)
            elif hasattr(result, 'output'):
                result_text = str(result.output)
            elif isinstance(result, str):
                result_text = result
            else:
                result_text = str(result)
            
            # Store result as string for now (will be structured later)
            response.agent_logs = [result_text]
            
            return response
            
        except Exception as e:
            return QueryResponse(
                response_id=response_id,
                query=query,
                status=QueryStatus.FAILED.value,
                error_message=f"Error processing query: {str(e)}",
                execution_time=time.time() - start_time
            )
    
    def handle_feedback(self, summary_id: str, rating: int, comments: str = "", 
                       improvement_requested: bool = False, 
                       session_id: Optional[str] = None) -> QueryResponse:
        """
        Handle user feedback on a summary.
        
        Args:
            summary_id: ID of the summary being rated
            rating: User rating (1-5)
            comments: Optional feedback comments
            improvement_requested: Whether user wants improved summary
            session_id: Optional session ID
            
        Returns:
            QueryResponse with updated results or acknowledgment
        """
        feedback_id = str(uuid.uuid4())
        response_id = str(uuid.uuid4())
        
        # Validate rating
        if not self.validator.validate_rating(rating):
            return QueryResponse(
                response_id=response_id,
                query=Query(query_id="", text=""),
                status=QueryStatus.FAILED.value,
                error_message="Invalid rating. Must be between 1 and 5."
            )
        
        # Validate comments
        if comments and not self.validator.validate_feedback_comment(comments):
            return QueryResponse(
                response_id=response_id,
                query=Query(query_id="", text=""),
                status=QueryStatus.FAILED.value,
                error_message="Invalid feedback comment."
            )
        
        # Create feedback object
        feedback = UserFeedback(
            feedback_id=feedback_id,
            summary_id=summary_id,
            rating=rating,
            comments=comments,
            improvement_requested=improvement_requested
        )
        
        # Update session if provided
        if session_id:
            self.session_manager.update_session(session_id, feedback=feedback)
        
        # TODO: Process feedback through Reflective Agent
        # For now, just acknowledge receipt
        response = QueryResponse(
            response_id=response_id,
            query=Query(query_id="", text=""),
            status=QueryStatus.COMPLETED.value,
            agent_logs=[
                f"Feedback received (Rating: {rating}/5)",
                f"Comments: {comments}" if comments else "No comments provided",
                "Improvement requested" if improvement_requested else "No improvement requested"
            ]
        )
        
        return response
    
    def get_session_state(self, session_id: str) -> Optional[dict]:
        """
        Get the current state of a session.
        
        Args:
            session_id: Session ID to retrieve
            
        Returns:
            Session history dict or None if not found
        """
        return self.session_manager.get_session_history(session_id)
    
    def cleanup_sessions(self) -> int:
        """
        Cleanup expired sessions.
        
        Returns:
            Number of sessions cleaned up
        """
        return self.session_manager.cleanup_expired()
