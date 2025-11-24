from crewai import Agent
from tools.rag_tool import rag_search_fallback

def search_logic(user_query: str) -> str:
    """Python fallback that directly queries Chromadb via rag_search_fallback."""
    docs = rag_search_fallback(user_query)
    if not docs:
        return "No documents found in the health RAG store."
    joined = "\n\n".join(docs)
    return f"Retrieved {len(docs)} document chunks:\n\n{joined}"

search_agent = Agent(
    name="Search Agent",
    role="Health Document Retriever",
    goal="Retrieve relevant health information from the RAG knowledge base.",
    backstory=(
        "You specialise in finding reliable medical information from curated sources "
        "stored in a vector database."
    ),
    verbose=True,
)
