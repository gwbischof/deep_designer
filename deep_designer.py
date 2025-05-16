#!/usr/bin/env python3
"""Stand-alone designer agent for design document generation."""
import os
import argparse
from pathlib import Path

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.utils.pprint import pprint_run_response
from agno.tools.reasoning import ReasoningTools

from tools import ask_customer, read_idea_file, update_design_json
from utils import initialize_design_json
from models import CompleteDesignDocument

# Designer prompt embedded directly in the code
DESIGNER_PROMPT = """First read the idea file with read_idea_file.

Transform the Customer's idea into an implementation-ready design document that satisfies them.

## Requirements
- Make sure to use reasoning tools to validate the design.
- You must ask the customer for feedback and approval before completing the work. All user feedback must be addressed.
- The resulting design document has to be detailed enough that it can be fully implemented without additional information. If the design document needs more details then assign more tasks to the agents."""


def create_designer_agent():
    """Creates a standalone designer agent for document creation."""
    # Create agent with direct arguments
    agent = Agent(
        name="Designer",
        role="Design document creator",
        description="Transform product ideas into implementation-ready design documents",
        instructions=[DESIGNER_PROMPT],
        show_tool_calls=True,
        add_name_to_instructions=True,
        model=Claude(id="claude-3-7-sonnet-latest"),
        tools=[
            ReasoningTools(add_instructions=True),
            ask_customer,
            read_idea_file,
            update_design_json,
        ],
        response_model=CompleteDesignDocument,
    )
    return agent


def parse_arguments():
    """Parses CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Design Document Generator - Stand-alone designer agent"
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
    root_dir_path = Path(os.path.dirname(os.path.abspath(__file__))) / "IDEA.md"
    if root_dir_path.exists():
        return str(root_dir_path)

    return str(root_dir_path)  # Return project root path even if it doesn't exist


def main():
    """Runs design document generation from IDEA.md content using a single agent."""
    # Check if IDEA.md exists
    idea_path = get_default_idea_path()
    if not Path(idea_path).exists():
        print(f"Error: IDEA.md not found. Expected at {idea_path}")
        print("Please create an IDEA.md file with your product idea.")
        return

    # Ensure DESIGN.json exists
    initialize_design_json()

    # Create the designer agent
    designer = create_designer_agent()

    print("📝 Stand-alone Design Document Generator")
    print("======================================")
    print(f"Using idea file: {idea_path}")

    # Run the designer agent
    response = designer.run(
        "Create a design document based on the idea in IDEA.md",
        show_full_reasoning=True,
    )

    # Use pprint_run_response for prettier output
    pprint_run_response(response, markdown=True)


if __name__ == "__main__":
    main()
