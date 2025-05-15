#!/usr/bin/env python3
"""Custom tools for Scrooge design document generator."""
import os
import sys
import json
import questionary
import markdown_to_json
from typing import List, Dict, Any, Optional
from pathlib import Path
from agno.tools import tool

# Import utils functions
from .utils import initialize_design_json, validate_design_json, load_prompt_text


@tool(show_result=True)
def ask_customer(questions: List[str], agent_name: str = "Unknown Agent") -> str:
    """Prompts the customer with questions and collects responses.

    Args:
        questions: List of question strings to ask sequentially.
        agent_name: Name of the agent using this tool.

    Returns:
        Formatted string with questions and responses.

    Note:
        Provide only ONE question in the list.
    """
    print(f"🛠️ [ask_customer] Called by {agent_name}")

    if not questions:
        return "No questions provided."

    # Initialize an empty string to store the Q&A
    qa_text = ""

    # Ask each question one at a time
    for i, question in enumerate(questions):
        print(f"\n[{agent_name}] asks: {question}")
        response = questionary.text(f"{question}").ask()

        # Add the Q&A to the result string
        qa_text += f"Question: {question}\nResponse: {response}\n\n"

        # Print a separator between questions (except after the last one)
        if i < len(questions) - 1:
            print("\n---\n")
    return qa_text.strip()


@tool(show_result=True)
def read_idea_file(file_path: str, agent_name: str = "Unknown Agent") -> str:
    """Reads product idea from file and converts markdown to JSON.

    Args:
        file_path: Path to file (typically IDEA.md).
        agent_name: Name of the agent using this tool.

    Returns:
        JSON string of markdown content or error message.
    """
    print(f"🛠️ [read_idea_file] Called by {agent_name} to read {file_path}")

    try:
        # Convert to Path object for better path handling
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read the file content
        with open(path, "r") as file:
            markdown_content = file.read()

        # Convert markdown to JSON
        json_content = markdown_to_json.jsonify(markdown_content)
        print("IDEA TOOL file successfully loaded")
        return json_content
    except FileNotFoundError as e:
        error_message = f"Error: {e}"
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"Error reading or converting file: {e}"
        print(error_message)
        return error_message


@tool(show_result=True)
def get_design_json(
    section: Optional[str] = None, agent_name: str = "Unknown Agent"
) -> str:
    """Gets content from DESIGN.json.

    Args:
        section: Optional section to retrieve (idea, marketing, architecture, design, tasks).
                If not provided, returns the entire file.
        agent_name: Name of the agent using this tool.

    Returns:
        JSON string of requested content.
    """
    section_info = "entire file" if section is None else f"section '{section}'"
    print(f"🛠️ [get_design_json] Called by {agent_name} to read {section_info}")

    try:
        # Validate DESIGN.json exists and is valid
        is_valid, error_msg, design_data = validate_design_json()

        if not is_valid:
            if "not found" in error_msg:
                # Initialize if not found
                initialize_design_json()
                # Re-validate after initialization
                is_valid, error_msg, design_data = validate_design_json()

                if not is_valid:
                    return json.dumps({"error": error_msg})
            else:
                return json.dumps({"error": error_msg})

        # Return only the requested section if specified
        if section:
            if section not in design_data:
                return json.dumps(
                    {"error": f"Section '{section}' not found in DESIGN.json"}
                )
            return json.dumps(design_data[section], indent=2)

        # Return the entire content
        return json.dumps(design_data, indent=2)

    except Exception as e:
        error_message = json.dumps({"error": f"Error accessing DESIGN.json: {str(e)}"})
        print(f"Error: {e}")
        return error_message


@tool(show_result=True)
def update_design_json(
    section: str, content: Dict[str, Any], agent_name: str = "Unknown Agent"
) -> str:
    """Updates a section in DESIGN.json.

    Args:
        section: Section to update (idea, marketing, architecture, design, tasks).
        content: JSON-compatible dict to store in the section.
        agent_name: Name of the agent using this tool.

    Returns:
        Success or error message.
    """
    print(
        f"🛠️ [update_design_json] Called by {agent_name} to update section '{section}'"
    )

    try:
        # Validate DESIGN.json exists and is valid
        is_valid, error_msg, design_data = validate_design_json()

        if not is_valid:
            if "not found" in error_msg:
                # Initialize if not found
                initialize_design_json()
                # Re-validate after initialization
                is_valid, error_msg, design_data = validate_design_json()

                if not is_valid:
                    return json.dumps({"error": error_msg})
            else:
                return json.dumps({"error": error_msg})

        # Verify the section exists
        if section not in design_data:
            return json.dumps(
                {"error": f"Section '{section}' not found in DESIGN.json"}
            )

        # Update the specified section
        design_data[section] = content

        # Write the updated content back to the file
        design_path = Path("DESIGN.json")
        with open(design_path, "w") as file:
            json.dump(design_data, file, indent=2)

        print(f"Section '{section}' updated successfully in DESIGN.json")
        return json.dumps({"success": f"Section '{section}' updated successfully"})

    except Exception as e:
        error_message = json.dumps({"error": f"Error updating DESIGN.json: {str(e)}"})
        print(f"Error: {e}")
        return error_message
