#!/usr/bin/env python3
"""Utility functions for Deep Designer document generator."""
import json
import os
import yaml
import re
from json.decoder import JSONDecodeError
from typing import Tuple, Dict, Any, Optional, List, Union
from pathlib import Path


def get_project_root() -> Path:
    """Returns the project root directory path."""
    # This function assumes it's being called from a module in the deep_designer package
    # Get the deep_designer package directory (where this file is located)
    deep_designer_dir = Path(__file__).parent.absolute()
    # The project root is one level up
    return deep_designer_dir.parent


def get_design_json_path() -> Path:
    """Returns the path to DESIGN.json."""
    return get_project_root() / "DESIGN.json"


def get_design_structure() -> Dict[str, Dict]:
    """Returns the initial structure for DESIGN.json."""
    return {"idea": {}, "marketing": {}, "architecture": {}, "design": {}, "tasks": {}}


def initialize_design_json() -> str:
    """Initializes DESIGN.json with empty structure in repository root.

    Returns:
        Path to the created file.
    """
    # Create DESIGN.json in current working directory (repo root)
    file_path = get_design_json_path()

    # Create initial structure
    design_structure = get_design_structure()

    # Write the structure to file if it doesn't exist or is empty
    if not file_path.exists() or file_path.stat().st_size == 0:
        with open(file_path, "w") as file:
            json.dump(design_structure, file, indent=2)
        print("Initialized DESIGN.json")
    else:
        print("DESIGN.json already exists")

    return str(file_path.absolute())


def get_prompts_dir() -> Path:
    """Returns the path to the prompts directory."""
    return Path(__file__).parent / "prompts"


def load_prompt(agent_name: str) -> Dict[str, Any]:
    """Loads a dotprompt file for an agent and returns Agent constructor parameters.

    Args:
        agent_name: Name of the agent (manager, marketing, architect, designer)

    Returns:
        Dictionary containing parameters directly mappable to Agent constructor

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        ValueError: If the prompt file has invalid format
    """
    prompts_dir = get_prompts_dir()
    prompt_file = prompts_dir / f"{agent_name}.prompt"

    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    with open(prompt_file, "r") as f:
        content = f.read()

    # Split frontmatter from content using the standard regex pattern
    frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)

    if not frontmatter_match:
        raise ValueError(
            f"Invalid prompt format in {prompt_file}, expected YAML frontmatter separated by ---"
        )

    yaml_content = frontmatter_match.group(1)
    prompt_content = frontmatter_match.group(2)

    try:
        # Parse the YAML frontmatter
        metadata = yaml.safe_load(yaml_content)

        # Process content for instructions based on agent type
        instructions = []
        if agent_name == "architect":
            # For architect, keep as a single string in a list (triple-quoted format)
            instructions = [prompt_content.strip()]
        else:
            # For other agents, convert to list of instructions
            content_lines = prompt_content.split("\n")
            for line in content_lines:
                # Clean up the line
                cleaned_line = line.strip()

                # Skip empty lines, headings, and bullet point markers
                if (
                    not cleaned_line
                    or cleaned_line.startswith("#")
                    or cleaned_line == "-"
                ):
                    continue

                # Remove bullet point marker if present
                if cleaned_line.startswith("- "):
                    cleaned_line = cleaned_line[2:]

                # Add the instruction
                if cleaned_line:
                    instructions.append(cleaned_line)

        # Map dotprompt fields to Agent constructor parameters
        agent_params = {
            "name": metadata.get("name", f"{agent_name.title()} Agent"),
            "description": metadata.get("description", ""),
            "instructions": instructions,
            "markdown": True,
            "add_name_to_instructions": True,
        }

        return agent_params
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in prompt frontmatter: {e}")


def validate_design_json() -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """Validates that DESIGN.json exists and contains valid JSON.

    Returns:
        Tuple containing:
        - bool: True if valid, False otherwise
        - Optional[str]: Error message if invalid, None if valid
        - Optional[Dict]: The parsed JSON data if valid, None if invalid
    """
    file_path = get_design_json_path()

    # Check if file exists
    if not file_path.exists():
        return False, f"DESIGN.json not found at {file_path.absolute()}", None

    # Check if file is empty
    if file_path.stat().st_size == 0:
        return False, "DESIGN.json exists but is empty", None

    # Attempt to parse JSON
    try:
        with open(file_path, "r") as file:
            data = json.load(file)

        # Verify that it has the expected structure
        expected_keys = get_design_structure().keys()
        missing_keys = [key for key in expected_keys if key not in data]

        if missing_keys:
            return (
                False,
                f"DESIGN.json is missing required sections: {', '.join(missing_keys)}",
                data,
            )

        return True, None, data

    except JSONDecodeError as e:
        return False, f"DESIGN.json contains invalid JSON: {str(e)}", None
    except Exception as e:
        return False, f"Error validating DESIGN.json: {str(e)}", None
