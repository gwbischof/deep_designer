#!/usr/bin/env python3
"""Custom tools for Scrooge design document generator."""
import json
import questionary
import markdown_to_json
from typing import Dict, Any, Optional
from pathlib import Path
from agno.tools import tool
from rich.prompt import Prompt

# Import utils functions
from utils import initialize_design_json, validate_design_json


@tool(show_result=True)
def ask_customer(question: str) -> str:
    """Prompts the customer with a single question and collects the response.

    Args:
        question: The question to ask the customer.

    Returns:
        Formatted string with the question and response.
    """
    print("🛠️ [ask_customer] Asking question.")

    if not question:
        return "No question provided."

    response = questionary.text(f"{question}").ask()
    #response = Prompt.ask(f"[bold] {question} [/bold]")

    # Format the question and response
    qa_text = f"Question: {question}\nResponse: {response}"

    return qa_text


@tool(show_result=True)
def read_idea_file(file_path: str) -> str:
    """Reads product idea from file and converts markdown to JSON.

    Args:
        file_path: Path to file (typically IDEA.md).

    Returns:
        JSON string of markdown content or error message.
    """
    print(f"🛠️ [read_idea_file] Reading {file_path}")

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
def get_design_json(section: Optional[str] = None) -> str:
    """Gets content from DESIGN.json.

    Args:
        section: Optional section to retrieve (idea, marketing, architecture, design, tasks).
                If not provided, returns the entire file.

    Returns:
        JSON string of requested content.
    """
    section_info = "entire file" if section is None else f"section '{section}'"
    print(f"🛠️ [get_design_json] Reading {section_info}")

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
def update_design_json(section: str, content: Dict[str, Any]) -> str:
    """Updates a section in DESIGN.json.

    Args:
        section: Section to update (idea, marketing, architecture, design, tasks).
        content: JSON-compatible dict to store in the section.

    Returns:
        Success or error message.
    """
    print(f"🛠️ [update_design_json] Updating section '{section}'")

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
