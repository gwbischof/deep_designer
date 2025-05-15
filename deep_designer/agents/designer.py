"""Designer agent for design document generation."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from ..utils import load_prompt


def create_design_agent():
    """Creates UI/UX designer agent."""
    # Load agent parameters from prompt file
    agent_params = load_prompt("designer")

    # Add role and model which aren't in the prompt
    agent_params.update(
        {
            "role": "User interface and experience design specialist",
            "model": OpenAIChat(id="gpt-4o"),
        }
    )

    agent = Agent(**agent_params)
    return agent
