"""Marketing agent for design document generation."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from ..utils import load_prompt


def create_marketing_agent():
    """Creates marketing agent for persona development."""
    # Load agent parameters from prompt file
    agent_params = load_prompt("marketing")

    # Add role and model which aren't in the prompt
    agent_params.update(
        {
            "role": "User persona specialist and audience analyst",
            "model": OpenAIChat(id="gpt-4o"),
        }
    )

    agent = Agent(**agent_params)
    return agent
