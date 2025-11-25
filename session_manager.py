"""
Session Manager

Manages user sessions and tracks query/feedback history.
"""
from typing import Dict, Optional
from datetime import datetime
import uuid

from models import SessionState, Query, UserFeedback


class SessionManager:
    """Manages user sessions."""
    
    def __init__(self, default_timeout: int = 30):
        """
        Initialize the session manager.
        
        Args:
            default_timeout: Default session timeout in minutes
        """
        self.sessions: Dict[str, SessionState] = {}
        self.timeout = default_timeout
    
    def create_session(self) -> str:
        """
        Create a new session.
        
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        session = SessionState(session_id=session_id)
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[SessionState]:
        """
        Get a session by ID.
        
        Args:
            session_id: Session ID to retrieve
            
        Returns:
            SessionState if found and not expired, None otherwise
        """
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        if session.is_expired(self.timeout):
            self.sessions.pop(session_id, None)
            return None
        
        return session
    
    def update_session(self, session_id: str, query: Optional[Query] = None, 
                      feedback: Optional[UserFeedback] = None) -> bool:
        """
        Update session with new query or feedback.
        
        Args:
            session_id: Session ID to update
            query: Query to add (optional)
            feedback: Feedback to add (optional)
            
        Returns:
            True if successful, False if session not found
        """
        session = self.get_session(session_id)
        
        if not session:
            return False
        
        if query:
            session.add_query(query)
        
        if feedback:
            session.add_feedback(feedback)
        
        return True
    
    def cleanup_expired(self) -> int:
        """
        Remove expired sessions.
        
        Returns:
            Number of sessions removed
        """
        expired_ids = [
            sid for sid, session in self.sessions.items()
            if session.is_expired(self.timeout)
        ]
        
        for sid in expired_ids:
            self.sessions.pop(sid)
        
        return len(expired_ids)
    
    def get_active_session_count(self) -> int:
        """
        Get count of active sessions.
        
        Returns:
            Number of active sessions
        """
        self.cleanup_expired()
        return len(self.sessions)
    
    def get_session_history(self, session_id: str) -> Dict:
        """
        Get complete history for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Dictionary with query and feedback history
        """
        session = self.get_session(session_id)
        
        if not session:
            return {"queries": [], "feedback": []}
        
        return {
            "session_id": session.session_id,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "queries": [q.to_dict() for q in session.query_history],
            "feedback": [f.to_dict() for f in session.feedback_history]
        }
