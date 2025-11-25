"""
Data Models for Health Research Agentic System

Contains all data classes used throughout the system for structured data handling.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class QueryStatus(Enum):
    """Status of a query processing."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Query:
    """Represents a user query."""
    query_id: str
    text: str
    timestamp: datetime = field(default_factory=datetime.now)
    user_context: Dict[str, Any] = field(default_factory=dict)
    session_id: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert query to dictionary."""
        return {
            "query_id": self.query_id,
            "text": self.text,
            "timestamp": self.timestamp.isoformat(),
            "user_context": self.user_context,
            "session_id": self.session_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Query':
        """Create Query from dictionary."""
        data_copy = data.copy()
        if isinstance(data_copy.get('timestamp'), str):
            data_copy['timestamp'] = datetime.fromisoformat(data_copy['timestamp'])
        return cls(**data_copy)


@dataclass
class Summary:
    """Represents a generated summary."""
    summary_id: str
    content: str
    source_docs: List[str] = field(default_factory=list)
    confidence: float = 0.0
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary."""
        return {
            "summary_id": self.summary_id,
            "content": self.content,
            "source_docs": self.source_docs,
            "confidence": self.confidence,
            "version": self.version,
            "created_at": self.created_at.isoformat()
        }
    
    def update_version(self) -> None:
        """Increment the version number."""
        self.version += 1
        self.created_at = datetime.now()


@dataclass
class UserFeedback:
    """Represents user feedback on a summary."""
    feedback_id: str
    summary_id: str
    rating: int
    comments: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    improvement_requested: bool = False
    specific_concerns: List[str] = field(default_factory=list)
    
    def validate_rating(self) -> bool:
        """Validate that rating is between 1 and 5."""
        return 1 <= self.rating <= 5
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert feedback to dictionary."""
        return {
            "feedback_id": self.feedback_id,
            "summary_id": self.summary_id,
            "rating": self.rating,
            "comments": self.comments,
            "timestamp": self.timestamp.isoformat(),
            "improvement_requested": self.improvement_requested,
            "specific_concerns": self.specific_concerns
        }


@dataclass
class ReflectionReport:
    """Represents a quality evaluation report from the Reflective Agent."""
    report_id: str
    summary_id: str
    coherence_score: float
    completeness_score: float
    factuality_confidence: float
    suggestions: List[str] = field(default_factory=list)
    requires_revision: bool = False
    evaluated_at: datetime = field(default_factory=datetime.now)
    
    def calculate_overall_score(self) -> float:
        """Calculate overall quality score (average of metrics)."""
        return (self.coherence_score + self.completeness_score + self.factuality_confidence) / 3.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "report_id": self.report_id,
            "summary_id": self.summary_id,
            "coherence_score": self.coherence_score,
            "completeness_score": self.completeness_score,
            "factuality_confidence": self.factuality_confidence,
            "suggestions": self.suggestions,
            "requires_revision": self.requires_revision,
            "evaluated_at": self.evaluated_at.isoformat(),
            "overall_score": self.calculate_overall_score()
        }


@dataclass
class QueryResponse:
    """Complete response to a user query."""
    response_id: str
    query: Query
    summary: Optional[Summary] = None
    reflection: Optional[ReflectionReport] = None
    status: str = QueryStatus.PENDING.value
    execution_time: float = 0.0
    agent_logs: List[str] = field(default_factory=list)
    error_message: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "response_id": self.response_id,
            "query": self.query.to_dict(),
            "summary": self.summary.to_dict() if self.summary else None,
            "reflection": self.reflection.to_dict() if self.reflection else None,
            "status": self.status,
            "execution_time": self.execution_time,
            "agent_logs": self.agent_logs,
            "error_message": self.error_message
        }
    
    def is_successful(self) -> bool:
        """Check if the query was processed successfully."""
        return self.status == QueryStatus.COMPLETED.value and not self.error_message


@dataclass
class SessionState:
    """Tracks a user session."""
    session_id: str
    query_history: List[Query] = field(default_factory=list)
    feedback_history: List[UserFeedback] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_activity: datetime = field(default_factory=datetime.now)
    
    def add_query(self, query: Query) -> None:
        """Add a query to the session history."""
        self.query_history.append(query)
        self.last_activity = datetime.now()
    
    def add_feedback(self, feedback: UserFeedback) -> None:
        """Add feedback to the session history."""
        self.feedback_history.append(feedback)
        self.last_activity = datetime.now()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if session has expired."""
        elapsed = (datetime.now() - self.last_activity).total_seconds() / 60
        return elapsed > timeout_minutes


@dataclass
class Document:
    """Represents a document from the knowledge base."""
    doc_id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: List[float] = field(default_factory=list)
    source: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary."""
        return {
            "doc_id": self.doc_id,
            "content": self.content,
            "metadata": self.metadata,
            "source": self.source,
            "created_at": self.created_at.isoformat()
        }
    
    def chunk(self, chunk_size: int = 500, overlap: int = 50) -> List['Document']:
        """
        Split document into chunks.
        
        Args:
            chunk_size: Size of each chunk in characters
            overlap: Number of overlapping characters between chunks
            
        Returns:
            List of Document chunks
        """
        chunks = []
        text = self.content
        start = 0
        chunk_num = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            chunk_doc = Document(
                doc_id=f"{self.doc_id}_chunk_{chunk_num}",
                content=chunk_text,
                metadata={**self.metadata, "chunk_num": chunk_num, "parent_id": self.doc_id},
                source=self.source,
                created_at=self.created_at
            )
            chunks.append(chunk_doc)
            
            start = end - overlap
            chunk_num += 1
        
        return chunks
