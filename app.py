"""Main orchestration for the health-research-agents system.

Tries to use CrewAI multi-agent workflow. If anything goes wrong
(e.g., missing API keys, version issues), it falls back to a pure
Python pipeline using the *_logic() helper functions from each agent module.
"""
from typing import Any

try:
    from crewai import Crew, Task
    CREW_AVAILABLE = True
except Exception:
    CREW_AVAILABLE = False

from agents.planner_agent import planner_agent, planner_logic
from agents.search_agent import search_agent, search_logic
from agents.summarize_agent import summarize_agent, summarize_logic
from agents.reflective_agent import reflective_agent, reflect_logic


def run_system(user_query: str) -> str:
    if not user_query or user_query.strip() == "":
        return "Please enter a health-related question to begin."

    if CREW_AVAILABLE:
        try:
            plan_task = Task(
                description=f"Plan research steps for the health query: '{user_query}'",
                expected_output="A clear list of research subtasks.",
                agent=planner_agent,
            )
            search_task = Task(
                description=(
                    "Using the plan, retrieve relevant health information from the vector store "
                    f"related to: '{user_query}'"
                ),
                expected_output="A set of relevant passages or document snippets.",
                agent=search_agent,
            )
            summarize_task = Task(
                description=(
                    "Summarize the retrieved health information into clear, concise language "
                    "with disclaimers that this is not medical advice."
                ),
                expected_output="A well-structured health research summary.",
                agent=summarize_agent,
            )
            reflect_task = Task(
                description=(
                    "Evaluate the summary for completeness, clarity, and potential issues. "
                    "Provide a short reflection report with recommendations."
                ),
                expected_output="A reflection report on the quality of the summary.",
                agent=reflective_agent,
            )

            crew = Crew(
                agents=[planner_agent, search_agent, summarize_agent, reflective_agent],
                tasks=[plan_task, search_task, summarize_task, reflect_task],
                verbose=True,
            )
            result: Any = crew.kickoff()
            return str(result)
        except Exception as e:
            fallback_header = (
                "CrewAI execution failed or is not fully configured.\n"
                f"Reason: {e}\n\n"
                "Falling back to simplified Python pipeline:\n\n"
            )
            return fallback_header + _python_fallback(user_query)
    else:
        return _python_fallback(user_query)


def _python_fallback(user_query: str) -> str:
    """Run a simple sequential pipeline without LLM calls."""
    plan = planner_logic(user_query)
    search_results = search_logic(user_query)
    summary = summarize_logic(search_results)
    reflection = reflect_logic(summary)

    parts = [
        "=== PLAN ===",
        plan,
        "",
        "=== RETRIEVED CONTENT ===",
        search_results,
        "",
        "=== SUMMARY ===",
        summary,
        "",
        "=== REFLECTION ===",
        reflection,
    ]
    return "\n".join(parts)
