#!/usr/bin/env python3
"""Multi-agent system for design document generation."""
import os
import sys
import argparse
from pathlib import Path

from deep_designer.agents import (
    create_marketing_agent,
    create_architect_agent,
    create_design_agent,
)
from deep_designer.tools import ask_customer, read_idea_file, update_design_json
from deep_designer.utils import load_prompt_text
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.utils.pprint import pprint_run_response


def create_design_document_team(debug=False):
    """Creates coordinated design document team."""
    # Create all specialized agents
    marketing = create_marketing_agent()
    architect = create_architect_agent()
    designer = create_design_agent()

    # Load team instructions
    instructions = load_prompt_text("team")

    # Create the team
    team = Team(
        debug_mode=debug,
        name="Design Document Generator",
        mode="coordinate",
        model=OpenAIChat("gpt-4o", temperature=0.1),
        tools=[ask_customer, read_idea_file],
        reasoning=False,
        enable_agentic_context=True,
        members=[
            marketing,
            architect,
            designer,
        ],
        instructions=[instructions],
        success_criteria="The resulting design document has to be detailed enough that it can be fully implemented without additional information.  The design document must meet ALL requirements of the idea. The customer must be happy about your design and approve the work.",
        show_members_responses=True,
        show_tool_calls=True,
        markdown=True,
    )

    return team


def parse_arguments():
    """Parses CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Design Document Generator - Create comprehensive design documents"
    )
    parser.add_argument(
        "--idea-file",
        "-i",
        type=str,
        default=None,
        help="Path to the IDEA.md file (defaults to ./IDEA.md in the root directory)",
    )
    return parser.parse_args()


def get_default_idea_path():
    """Finds IDEA.md file location."""
    # First check current directory
    current_dir_path = Path("IDEA.md")
    if current_dir_path.exists():
        return str(current_dir_path.absolute())

    # Then check project root
    root_dir_path = (
        Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) / "IDEA.md"
    )
    if root_dir_path.exists():
        return str(root_dir_path)

    return str(root_dir_path)  # Return project root path even if it doesn't exist


def main():
    """Runs design document generation from IDEA.md content."""
    # Parse command line arguments
    args = parse_arguments()

    # Check if IDEA.md exists
    idea_path = get_default_idea_path()
    if not Path(idea_path).exists():
        print(f"Error: IDEA.md not found. Expected at {idea_path}")
        print("Please create an IDEA.md file with your product idea.")
        return

    team = create_design_document_team(debug=False)

    print("📝 Design Document Generator")

    # Pass instruction to the team to use the idea file
    response = team.run("Create a design document based on the idea in IDEA.md")

    # Use pprint_run_response for prettier output
    pprint_run_response(response, markdown=True)


if __name__ == "__main__":
    main()
