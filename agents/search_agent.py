import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_agent import BaseAgent
from tools.rag_tool import rag_search_fallback
from typing import Any, List
from llm_config import get_llm_config

try:
    from crewai import Agent
    CREW_AVAILABLE = True
except ImportError:
    CREW_AVAILABLE = False


class SearchAgent(BaseAgent):
    """Agent responsible for retrieving documents from RAG knowledge base."""
    
    def __init__(self, top_k: int = 5):
        super().__init__(
            agent_id="search_001",
            name="Search Agent",
            role="Health Document Retriever",
            llm_model="mistral-small",
            verbose=True
        )
        self.top_k = top_k
        self.search_strategy = "vector_similarity"
    
    def process(self, input_data: Any) -> str:
        """
        Process a query and retrieve relevant documents.
        
        Args:
            input_data: User query string
            
        Returns:
            Retrieved documents as formatted string
        """
        if not isinstance(input_data, str):
            raise ValueError("SearchAgent expects string input")
        
        query = input_data.strip()
        if len(query) < 3:
             return "Query too short. Please provide more specific health-related keywords."

        self.log_activity(f"Searching for: {query}")
        
        docs = self.retrieve_documents(query)
        return docs
    
    def retrieve_documents(self, query: str) -> str:
        """
        Retrieve relevant documents from RAG store.
        
        Args:
            query: Search query
            
        Returns:
            Formatted document results
        """
        docs = self.query_vector_db(query, self.top_k)
        
        if not docs:
            self.log_activity("No documents found")
            return "No documents found in the health RAG store."
        
        self.log_activity(f"Retrieved {len(docs)} documents")
        joined = "\n\n".join(docs)
        return f"Retrieved {len(docs)} document chunks:\n\n{joined}"
    
    def query_vector_db(self, query: str, k: int) -> List[str]:
        """
        Query the vector database.
        
        Args:
            query: Search query
            k: Number of results to return
            
        Returns:
            List of document contents
        """
        return rag_search_fallback(query, k)
    
    def rank_results(self, docs: List[str]) -> List[str]:
        """Rank retrieved documents (simple pass-through for now)."""
        return docs


# Legacy fallback function for compatibility
def search_logic(user_query: str) -> str:
    """Python fallback that directly queries Chromadb via rag_search_fallback."""
    agent = SearchAgent()
    return agent.process(user_query)


# CrewAI agent for compatibility - created lazily to avoid import errors
search_agent = None

def get_search_agent():
    """Get or create the search agent."""
    global search_agent
    if CREW_AVAILABLE and search_agent is None:
        llm = get_llm_config()
        search_agent = Agent(
            name="Search Agent",
            role="Health Document Retriever",
            goal="Retrieve relevant health information from the RAG knowledge base to answer complex user queries.",
            backstory=(
                "You specialise in finding reliable medical information from curated sources "
                "stored in a vector database. You are capable of handling queries about various "
                "health topics including diseases, prevention, mental health, and lifestyle choices."
            ),
            llm=llm,
            verbose=True,
        )
    return search_agent
