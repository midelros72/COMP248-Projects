"""
Input Validator

Validates and sanitizes user input before processing.
"""
from typing import Optional
import re


class InputValidator:
    """Validates user queries and other inputs."""
    
    def __init__(self, max_length: int = 1000, min_length: int = 3):
        """
        Initialize the validator.
        
        Args:
            max_length: Maximum allowed query length
            min_length: Minimum allowed query length
        """
        self.max_length = max_length
        self.min_length = min_length
        
        # Patterns that might indicate malicious input
        self.forbidden_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',               # JavaScript protocol
            r'on\w+\s*=',                # Event handlers
        ]
    
    def validate_query(self, query: str) -> bool:
        """
        Validate a user query.
        
        Args:
            query: Query string to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not query or not isinstance(query, str):
            return False
        
        query = query.strip()
        
        # Check length
        if not self.check_length(query):
            return False
        
        # Check for dangerous patterns
        if not self.check_safety(query):
            return False
        
        return True
    
    def sanitize_input(self, input_str: str) -> str:
        """
        Sanitize input by removing potentially harmful content.
        
        Args:
            input_str: Input string to sanitize
            
        Returns:
            Sanitized string
        """
        if not input_str:
            return ""
        
        # Remove HTML/script tags
        sanitized = re.sub(r'<[^>]+>', '', input_str)
        
        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')
        
        # Normalize whitespace
        sanitized = ' '.join(sanitized.split())
        
        return sanitized.strip()
    
    def check_length(self, text: str) -> bool:
        """
        Check if text length is within acceptable bounds.
        
        Args:
            text: Text to check
            
        Returns:
            True if length is acceptable, False otherwise
        """
        length = len(text.strip())
        return self.min_length <= length <= self.max_length
    
    def check_safety(self, text: str) -> bool:
        """
        Check text for potentially dangerous patterns.
        
        Args:
            text: Text to check
            
        Returns:
            True if safe, False if dangerous patterns found
        """
        text_lower = text.lower()
        
        for pattern in self.forbidden_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return False
        
        return True
    
    def validate_rating(self, rating: int) -> bool:
        """
        Validate a user rating.
        
        Args:
            rating: Rating value to validate
            
        Returns:
            True if valid (1-5), False otherwise
        """
        return isinstance(rating, int) and 1 <= rating <= 5
    
    def validate_feedback_comment(self, comment: str) -> bool:
        """
        Validate feedback comment.
        
        Args:
            comment: Comment text to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not comment:
            return True  # Comments are optional
        
        return self.check_length(comment) and self.check_safety(comment)
