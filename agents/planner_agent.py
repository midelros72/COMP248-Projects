from crewai import Agent

def planner_logic(user_query: str) -> str:
    """Simple python fallback planner logic used if CrewAI fails."""
    return (
        f"Plan for query: '{user_query}'.\n"
        "- Identify key medical topic.\n"
        "- Search trusted health sources.\n"
        "- Extract symptoms, causes, treatments.\n"
        "- Summarize in plain language with disclaimers."
    )

planner_agent = Agent(
    name="Planner Agent",
    role="Task Planner",
    goal="Break down health research questions into clear subtasks.",
    backstory=(
        "You are an experienced research coordinator who knows how to structure "
        "health-related research tasks for other agents."
    ),
    verbose=True,
)
