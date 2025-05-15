"""Designer agent for design document generation."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from ..utils import load_prompt_text


def create_design_agent():
    """Creates UI/UX designer agent."""
    # Load prompt text directly from the prompt file
    instructions = load_prompt_text("designer")

    # Create agent with direct arguments
    agent = Agent(
        name="UI/UX Designer",
        role="User interface and experience design specialist",
        description="Design interfaces for product requirements",
        instructions=[instructions],
        markdown=True,
        add_name_to_instructions=True,
        model=OpenAIChat(id="gpt-4o")
    )
    return agent
