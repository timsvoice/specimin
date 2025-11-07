#!/usr/bin/env python3
"""
Workspace management for Specimin evaluation framework.
Creates version-based run directories for storing evaluation artifacts.
"""

import json
import os
import sys
from pathlib import Path


def get_plugin_version():
    """
    Read the version from the plugin.json file.

    Returns:
        str: Version string from plugin.json

    Raises:
        SystemExit: If plugin.json cannot be read or version is missing
    """
    # Navigate to project root to find .claude-plugin/plugin.json
    eval_dir = Path(__file__).parent
    project_root = eval_dir.parent.parent
    plugin_json_path = project_root / ".claude-plugin" / "plugin.json"

    try:
        with open(plugin_json_path, 'r') as f:
            plugin_data = json.load(f)
            version = plugin_data.get('version')
            if not version:
                print("Error: 'version' field not found in plugin.json", file=sys.stderr)
                sys.exit(1)
            return version
    except FileNotFoundError:
        print(f"Error: plugin.json not found at {plugin_json_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in plugin.json: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading plugin.json: {e}", file=sys.stderr)
        sys.exit(1)


def create_run_directory():
    """
    Create a version-based run directory for evaluation artifacts.

    Returns:
        str: Path to the created run directory
    """
    # Get version from plugin.json
    version = get_plugin_version()

    # Create run directory path based on version
    eval_dir = Path(__file__).parent
    runs_dir = eval_dir / "runs"
    run_dir = runs_dir / f"v{version}"

    # Create directory if it doesn't exist
    try:
        run_dir.mkdir(parents=True, exist_ok=True)
        return str(run_dir)
    except OSError as e:
        print(f"Error creating run directory: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point when run as script."""
    run_dir = create_run_directory()
    print(run_dir)


if __name__ == "__main__":
    main()
