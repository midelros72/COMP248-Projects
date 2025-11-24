from crewai import Agent

def summarize_logic(retrieved_text: str) -> str:
    """Very simple python summarization fallback."""
    if not retrieved_text or retrieved_text.strip() == "":
        return "No content available to summarize."
    snippet = retrieved_text[:800]
    return (
        "Summary (fallback mode):\n"
        "This content discusses health-related information gathered from the RAG store.\n"
        f"Key excerpt:\n{snippet}"
    )

summarize_agent = Agent(
    name="Summarization Agent",
    role="Health Research Summarizer",
    goal="Summarize retrieved health content into clear, concise language.",
    backstory=(
        "You are skilled at turning dense medical information into accessible research "
        "summaries for analysts."
    ),
    verbose=True,
)
