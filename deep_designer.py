#!/usr/bin/env python3
"""Multi-agent system for design document generation."""
import os
import sys
import argparse
from pathlib import Path

from deep_designer.agents import (
    create_manager_agent,
    create_marketing_agent,
    create_architect_agent,
    create_design_agent,
)
from deep_designer.tools import ask_questions, read_idea_file, update_design_json
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.utils.pprint import pprint_run_response


def create_design_document_team(debug=False):
    """Creates coordinated design document team."""
    # Create all specialized agents
    manager = create_manager_agent()
    marketing = create_marketing_agent()
    architect = create_architect_agent()
    designer = create_design_agent()

    # Create the team with the manager as coordinator
    team = Team(
        debug_mode=debug,
        name="Design Document Generator",
        mode="coordinate",  # Use coordinate mode
        model=OpenAIChat("gpt-4o", temperature=0.7),
        tools=[ask_questions, read_idea_file, update_design_json],  # Add custom tools
        enable_agentic_context=True,
        members=[
            manager,  # First member acts as coordinator in coordinate mode
            marketing,
            architect,
            designer,
        ],
        instructions=[
            "You are the Design Document Manager coordinating a detailed design document creation process:",
            "1. Manager: First read the idea file with read_idea_file('./IDEA.md', 'Manager') → Save idea to DESIGN.json using update_design_json('idea', {'description': '...idea text...'}, 'Manager') → Ask ONE clarifying question",
            "2. Marketing Expert: Create 3 user personas → Ask ONE question → Marketing Expert saves to DESIGN.json using update_design_json('marketing', {'personas': [...]}, 'Marketing Expert') ",
            "3. Technical Architect: Design system architecture → Ask ONE question → Technical Architect saves to DESIGN.json using update_design_json('architecture', {'components': [...]}, 'Technical Architect') ",
            "4. UI/UX Designer: Create designs (if needed) → Ask ONE question→ UI/UX Designer saves to DESIGN.json using update_design_json('design', {'screens': [...]}, 'UI/UX Designer') ",
            "5. Manager: Compile all contributions into final document",
            "RULES:",
            "- IMPORTANT: Always start by reading IDEA.md with read_idea_file('./IDEA.md', 'Manager')",
            "- Each specialist may ask exactly ONE high-priority question via ask_questions(['Your question here?'], 'Your Agent Name')",
            "- Always include your agent name when calling any tool",
            "- Each specialist must save their own work to their corresponding section in DESIGN.json",
            "- The Manager saves the initial idea to the 'idea' section",
            "- Ensure all components integrate cohesively in final document",
        ],
        success_criteria="A complete design document has been created with marketing, architecture, and UI/UX contributions, with human approval at each stage.",
        show_members_responses=True,
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
    print("===========================")
    print(f"Using idea file: {idea_path}")

    # Pass instruction to the team to use the idea file
    response = team.run("Create a design document based on the idea in IDEA.md")

    # Use pprint_run_response for prettier output
    pprint_run_response(response, markdown=True)


if __name__ == "__main__":
    main()