import ast
from pathlib import Path

def check_syntax(source_code: str) -> dict:
    """Check Python source code for syntax errors without executing it."""

    try:
        ast.parse(source_code)
    except SyntaxError as error:
        return {
            "valid": False,
            "line": error.lineno,
            "message": error.msg,
        }

    return {
        "valid": True,
        "line": None,
        "message": "No syntax errors found.",
    }

def check_file_syntax(file_path: str | Path) -> dict:
    """Read a Python file and check its syntax without executing it."""

    source_code = Path(file_path).read_text(encoding="utf-8")

    return check_syntax(source_code)

