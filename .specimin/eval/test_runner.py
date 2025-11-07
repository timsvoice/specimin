#!/usr/bin/env python3
"""
Test execution module for Specimin evaluation framework.
Runs pytest on generated code and captures results.
"""

import sys
import subprocess
import json
from pathlib import Path


def run_test(test_dir):
    """
    Run pytest on code and test files in the given directory.

    Args:
        test_dir (str): Directory containing code.py and test.py

    Returns:
        dict: Test result with keys:
            - test_id (str): Test case identifier
            - passed (bool): Whether all tests passed
            - error_type (str): Type of error if failed
            - error_message (str): Error details if failed
            - stdout (str): Standard output
            - stderr (str): Standard error
    """
    test_dir = Path(test_dir)
    test_id = test_dir.name

    code_file = test_dir / "code.py"
    test_file = test_dir / "test.py"

    # Check if files exist
    if not code_file.exists():
        return {
            "test_id": test_id,
            "passed": False,
            "error_type": "missing_file",
            "error_message": f"Code file not found: {code_file}",
            "stdout": "",
            "stderr": ""
        }

    if not test_file.exists():
        return {
            "test_id": test_id,
            "passed": False,
            "error_type": "missing_file",
            "error_message": f"Test file not found: {test_file}",
            "stdout": "",
            "stderr": ""
        }

    # First, check if the code has syntax errors
    try:
        with open(code_file, 'r') as f:
            code_content = f.read()
        compile(code_content, str(code_file), 'exec')
    except SyntaxError as e:
        return {
            "test_id": test_id,
            "passed": False,
            "error_type": "syntax_error",
            "error_message": f"Syntax error in generated code: {e}",
            "stdout": "",
            "stderr": str(e)
        }

    # Run pytest
    try:
        # Modify test file to import the implementation module
        # This assumes test code uses `implementation` as module name
        temp_test_file = test_dir / "test_modified.py"
        with open(test_file, 'r') as f:
            test_content = f.read()

        # Inject import statement
        modified_test = f"""
import sys
from pathlib import Path

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import implementation as a module
import code as implementation

{test_content}
"""
        with open(temp_test_file, 'w') as f:
            f.write(modified_test)

        # Run pytest
        result = subprocess.run(
            ["python3", "-m", "pytest", str(temp_test_file), "-v"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(test_dir)
        )

        # Clean up temp file
        temp_test_file.unlink()

        if result.returncode == 0:
            return {
                "test_id": test_id,
                "passed": True,
                "error_type": None,
                "error_message": None,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        else:
            # Determine error type from output
            error_type = "assertion_failure"
            if "ImportError" in result.stderr or "ModuleNotFoundError" in result.stderr:
                error_type = "import_error"
            elif "AttributeError" in result.stderr:
                error_type = "missing_function"

            return {
                "test_id": test_id,
                "passed": False,
                "error_type": error_type,
                "error_message": result.stderr or result.stdout,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

    except subprocess.TimeoutExpired:
        return {
            "test_id": test_id,
            "passed": False,
            "error_type": "timeout",
            "error_message": "Test execution timed out after 30 seconds",
            "stdout": "",
            "stderr": ""
        }
    except Exception as e:
        return {
            "test_id": test_id,
            "passed": False,
            "error_type": "execution_error",
            "error_message": str(e),
            "stdout": "",
            "stderr": str(e)
        }


def main():
    """Main entry point when run as script."""
    if len(sys.argv) != 2:
        print("Usage: test_runner.py <test_directory>", file=sys.stderr)
        sys.exit(1)

    test_dir = sys.argv[1]
    result = run_test(test_dir)

    # Print JSON result
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
