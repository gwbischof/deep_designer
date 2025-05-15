#!/usr/bin/env python3
"""Validation script for DESIGN.json."""
import sys
import json
from pathlib import Path

# Add parent directory to Python path to import from deep_designer module
sys.path.append(str(Path(__file__).parent.parent))
from deep_designer.utils import validate_design_json


def main():
    """Validates DESIGN.json and reports status."""
    print("Validating DESIGN.json...")
    is_valid, error_msg, data = validate_design_json()

    if is_valid:
        print("✅ DESIGN.json is valid")
        print("\nStructure:")
        for section, content in data.items():
            content_size = len(json.dumps(content))
            status = "empty" if content_size <= 2 else "populated"
            print(f"  - {section}: {status} ({content_size} bytes)")
        return 0
    else:
        print(f"❌ DESIGN.json validation failed: {error_msg}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
