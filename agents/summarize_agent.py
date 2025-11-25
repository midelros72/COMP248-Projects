import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_agent import BaseAgent
from typing import Any, List
from llm_config import get_llm_config

try:
    from crewai import Agent
    CREW_AVAILABLE = True
except ImportError:
    CREW_AVAILABLE = False


class SummarizationAgent(BaseAgent):
    """Agent responsible for summarizing retrieved health information."""
    
    def __init__(self, max_length: int = 1000):
        super().__init__(
            agent_id="summarizer_001",
            name="Summarization Agent",
            role="Health Research Summarizer",
            llm_model="gpt-4o-mini",
            verbose=True
        )
        self.max_length = max_length
        self.style = "accessible"
        self.temperature = 0.7
    
    def process(self, input_data: Any) -> str:
        """
        Process retrieved text and generate summary.
        
        Args:
            input_data: Retrieved text to summarize
            
        Returns:
            Summary text
        """
        if not isinstance(input_data, str):
            raise ValueError("SummarizationAgent expects string input")
        
        retrieved_text = input_data
        self.log_activity(f"Summarizing {len(retrieved_text)} characters of text")
        
        summary = self.summarize(retrieved_text)
        return summary
    
    def summarize(self, retrieved_text: str) -> str:
        """
        Create a summary from retrieved documents.
        
        Args:
            retrieved_text: Text to summarize
            
        Returns:
            Formatted summary
        """
        if not retrieved_text or retrieved_text.strip() == "":
            return "No content available to summarize."
        
        # Simple summarization - take key portions
        snippet = retrieved_text[:self.max_length]
        
        summary = (
            "Health Research Summary\n"
            "=" * 50 + "\n\n"
            "This summary presents health-related information gathered from trusted medical sources.\n\n"
            "Key Information:\n"
            f"{snippet}\n\n"
            "Important Disclaimer:\n"
            "This information is for research purposes only and does not constitute medical advice. "
            "Please consult with qualified healthcare professionals for medical guidance.\n"
        )
        
        self.log_activity("Summary generated successfully")
        return summary
    
    def format_output(self, summary: str) -> str:
        """Format the summary output."""
        return summary
    
    def re_summarize(self, retrieved_text: str, suggestions: List[str]) -> str:
        """
        Re-create summary incorporating feedback suggestions.
        
        Args:
            retrieved_text: Original retrieved text
            suggestions: List of improvement suggestions
            
        Returns:
            Improved summary
        """
        self.log_activity(f"Re-summarizing with {len(suggestions)} suggestions")
        
        # For now, append suggestions to summary
        base_summary = self.summarize(retrieved_text)
        
        if suggestions:
            improvements = "\n\nIncorporated Improvements:\n" + "\n".join(f"- {s}" for s in suggestions)
            return base_summary + improvements
        
        return base_summary


# Legacy fallback function for compatibility
def summarize_logic(retrieved_text: str) -> str:
    """Very simple python summarization fallback."""
    agent = SummarizationAgent()
    return agent.process(retrieved_text)


# CrewAI agent for compatibility - created lazily to avoid import errors
summarize_agent = None

def get_summarize_agent():
    """Get or create the summarize agent."""
    global summarize_agent
    if CREW_AVAILABLE and summarize_agent is None:
        llm = get_llm_config()
        summarize_agent = Agent(
            name="Summarization Agent",
            role="Health Research Summarizer",
            goal="Summarize retrieved health content into clear, concise language.",
            backstory=(
                "You are skilled at turning dense medical information into accessible research "
                "summaries for analysts."
            ),
            llm=llm,
            verbose=True,
        )
    return summarize_agent
