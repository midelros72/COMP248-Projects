import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_agent import BaseAgent
from typing import Any, List, Dict
from llm_config import get_llm_config

try:
    from crewai import Agent
    CREW_AVAILABLE = True
except ImportError:
    CREW_AVAILABLE = False


class PlannerAgent(BaseAgent):
    """Agent responsible for planning and breaking down research tasks."""
    
    def __init__(self):
        super().__init__(
            agent_id="planner_001",
            name="Planner Agent",
            role="Task Planner",
            llm_model="gpt-4o-mini",
            verbose=True
        )
        self.strategies = [
            "identify_topic",
            "search_sources",
            "extract_information",
            "summarize_findings"
        ]
    
    def process(self, input_data: Any) -> str:
        """
        Process a query and create a research plan.
        
        Args:
            input_data: User query string
            
        Returns:
            Research plan as string
        """
        if not isinstance(input_data, str):
            raise ValueError("PlannerAgent expects string input")
        
        query = input_data
        self.log_activity(f"Creating plan for query: {query}")
        
        plan = self.create_plan(query)
        return plan
    
    def create_plan(self, query: str) -> str:
        """
        Create a structured research plan.
        
        Args:
            query: User query
            
        Returns:
            Formatted plan
        """
        return (
            f"Research Plan for: '{query}'\n\n"
            "Step 1: Identify key medical topic and concepts\n"
            "Step 2: Search trusted health sources (CDC, WHO, PubMed)\n"
            "Step 3: Extract relevant information:\n"
            "  - Symptoms and signs\n"
            "  - Causes and risk factors\n"
            "  - Treatment options\n"
            "  - Prevention measures\n"
            "Step 4: Summarize findings in plain language\n"
            "Step 5: Add medical disclaimers\n"
        )
    
    def prioritize_tasks(self, tasks: List[str]) -> List[str]:
        """Prioritize a list of tasks."""
        # Simple priority: maintain order for now
        return tasks


# Legacy fallback function for compatibility
def planner_logic(user_query: str) -> str:
    """Simple python fallback planner logic used if CrewAI fails."""
    agent = PlannerAgent()
    return agent.process(user_query)


# CrewAI agent for compatibility - created lazily to avoid import errors
planner_agent = None

def get_planner_agent():
    """Get or create the planner agent."""
    global planner_agent
    if CREW_AVAILABLE and planner_agent is None:
        llm = get_llm_config()
        
        # Skip agent creation if no valid LLM
        if llm is None:
            return None
            
        planner_agent = Agent(
            name="Planner Agent",
            role="Task Planner",
            goal="Break down health research questions into clear subtasks.",
            backstory=(
                "You are an experienced research coordinator who knows how to structure "
                "health-related research tasks for other agents."
            ),
            llm=llm,
            verbose=True,
        )
    return planner_agent
