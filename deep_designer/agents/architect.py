"""Architect agent for design document generation."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from ..utils import load_prompt


def create_architect_agent():
    """Creates architect agent for technical design."""
    # Load agent parameters from prompt file
    agent_params = load_prompt("architect")

    # Add role and model which aren't in the prompt
    agent_params.update(
        {
            "role": "Software architecture and system design expert",
            "model": OpenAIChat(id="gpt-4o"),
        }
    )

    agent = Agent(**agent_params)
    return agent
