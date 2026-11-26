from pathlib import Path
from analyzer.syntax import check_syntax, check_file_syntax

def test_valid_python():
    code = "age = 15\nprint(age)"
    result = check_syntax(code)

    assert result["valid"] is True
    assert result["line"] is None


def test_missing_colon():
    code = "if age >= 13\n    print('Teen')"
    result = check_syntax(code)

    assert result["valid"] is False
    assert result["line"] == 1


def test_code_is_not_executed():
    code = "raise RuntimeError('Should never run')"
    result = check_syntax(code)

    assert result["valid"] is True

def test_valid_python_file():
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "sample_submissions" / "student_001.py"

    result = check_file_syntax(file_path)

    assert result["valid"] is True
    assert result["line"] is None
    assert result["message"] == "No syntax errors found."

def test_invalid_python_file():
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "sample_submissions" / "student_002.py"

    result = check_file_syntax(file_path)

    assert result["valid"] is False
    assert result["line"] == 3
    assert result["message"] == "expected ':'"
