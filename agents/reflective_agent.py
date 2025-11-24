from crewai import Agent

def reflect_logic(summary_text: str) -> str:
    """Simple reflection that scores the summary on a few axes."""
    if not summary_text or summary_text.strip() == "":
        return "Reflection: No summary provided to evaluate."

    length_score = 4 if len(summary_text) > 300 else 2
    completeness = "likely incomplete" if length_score < 3 else "probably reasonably complete"

    report = (
        "Reflection Report (fallback mode):\n"
        f"- Approx length-based completeness: {completeness}.\n"
        "- Coherence: assumed moderate (manual check still needed).\n"
        "- Factuality: depends on source quality (RAG inputs).\n"
        "Recommendation: Double-check critical medical claims with primary sources."
    )
    return report

reflective_agent = Agent(
    name="Reflective Agent",
    role="Quality Reviewer",
    goal="Evaluate summaries for completeness, clarity, and potential issues.",
    backstory=(
        "You review health summaries to flag potential gaps, ambiguity, or risky claims, "
        "and suggest improvements."
    ),
    verbose=True,
)
