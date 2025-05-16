"""Marketing agent for design document generation."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from ..utils import load_prompt_text


def create_marketing_agent():
    """Creates marketing agent for persona development."""
    # Load prompt text directly from the prompt file
    instructions = load_prompt_text("marketing")

    # Create agent with direct arguments
    agent = Agent(
        name="Marketing Expert",
        role="User persona specialist and audience analyst",
        description="Create market analysis and user personas for product ideas",
        instructions=[instructions],
        markdown=True,
        add_name_to_instructions=True,
        model=OpenAIChat(id="gpt-4o"),
    )
    return agent
