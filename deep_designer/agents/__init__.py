"""Agent module for Scrooge design document generator."""

from .manager import create_manager_agent
from .marketing import create_marketing_agent
from .architect import create_architect_agent
from .designer import create_design_agent

__all__ = [
    "create_manager_agent",
    "create_marketing_agent",
    "create_architect_agent",
    "create_design_agent",
]
