"""Manager agent for design document generation."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from ..utils import load_prompt


def create_manager_agent():
    """Creates manager agent for document coordination."""
    # Load agent parameters from prompt file
    agent_params = load_prompt("manager")

    # Add role and model which aren't in the prompt
    agent_params.update(
        {
            "role": "Design document coordinator and process manager",
            "model": OpenAIChat(id="gpt-4o"),
        }
    )

    agent = Agent(**agent_params)
    return agent
