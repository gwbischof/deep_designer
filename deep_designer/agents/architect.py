"""Architect agent for design document generation."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from ..utils import load_prompt_text


def create_architect_agent():
    """Creates architect agent for technical design."""
    # Load prompt text directly from the prompt file
    instructions = load_prompt_text("architect")

    # Create agent with direct arguments
    agent = Agent(
        name="Technical Architect",
        role="Software architecture and system design expert",
        description="Create technical architecture based on product requirements",
        instructions=[instructions],
        markdown=True,
        add_name_to_instructions=True,
        model=OpenAIChat(id="gpt-4o"),
    )
    return agent
