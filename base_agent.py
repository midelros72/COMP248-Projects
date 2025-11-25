"""
Base Agent Abstract Class

Provides common interface and functionality for all agents in the system.
All agent classes should inherit from this base class.
"""
from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime


class BaseAgent(ABC):
    """Abstract base class for all agents in the system."""
    
    def __init__(self, agent_id: str, name: str, role: str, llm_model: str = "gpt-4o-mini", verbose: bool = True):
        """
        Initialize the base agent.
        
        Args:
            agent_id: Unique identifier for the agent
            name: Display name of the agent
            role: Role description of the agent
            llm_model: LLM model to use (default: gpt-4o-mini)
            verbose: Whether to log activities (default: True)
        """
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.llm_model = llm_model
        self.verbose = verbose
        self.activity_log = []
    
    def execute(self, input_data: Any) -> Any:
        """
        Execute the agent's main task.
        
        Args:
            input_data: Input data for the agent to process
            
        Returns:
            Processed output from the agent
        """
        if not self.validate_input(input_data):
            self.log_activity(f"Invalid input received: {type(input_data)}")
            raise ValueError(f"Invalid input for agent {self.name}")
        
        self.log_activity(f"Executing task with input type: {type(input_data).__name__}")
        result = self.process(input_data)
        self.log_activity(f"Task completed successfully")
        return result
    
    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data before processing.
        
        Args:
            input_data: Input to validate
            
        Returns:
            True if input is valid, False otherwise
        """
        if input_data is None:
            return False
        return True
    
    def log_activity(self, message: str) -> None:
        """
        Log an activity message.
        
        Args:
            message: Message to log
        """
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{self.name}] {message}"
        self.activity_log.append(log_entry)
        
        if self.verbose:
            print(log_entry)
    
    def get_activity_log(self) -> list:
        """
        Get the agent's activity log.
        
        Returns:
            List of log entries
        """
        return self.activity_log.copy()
    
    def clear_log(self) -> None:
        """Clear the activity log."""
        self.activity_log = []
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        """
        Process the input and return output.
        This method must be implemented by subclasses.
        
        Args:
            input_data: Input data to process
            
        Returns:
            Processed output
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.agent_id}, name={self.name}, role={self.role})"
