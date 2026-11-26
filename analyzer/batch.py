
from pathlib import Path

from analyzer.syntax import check_syntax
from analyzer.privacy import scan_for_emails, scan_for_student_ids
from analyzer.structure import analyze_structure


def analyze_source(source_code: str, submission_id: str) -> dict:
    """Analyze one Python submission without executing it."""

    # Check syntax
    syntax_result = check_syntax(source_code)

    # Screen for possible personal information
    privacy_findings = (
        scan_for_emails(source_code)
        + scan_for_student_ids(source_code)
    )

    # Analyze programming constructs
    structure_result = analyze_structure(source_code)

    return {
        "submission_id": submission_id,
        **syntax_result,
        "privacy_flags": len(privacy_findings),
        "privacy_review_required": bool(privacy_findings),
        "if_branches": structure_result["if_branches"],
        "for_loops": structure_result["for_loops"],
        "while_loops": structure_result["while_loops"],
        "functions": structure_result["functions"],
    }


def analyze_folder(folder_path: str | Path) -> list[dict]:
    """Analyze Python files in a folder."""

    folder = Path(folder_path)
    results = []

    python_files = sorted(folder.glob("*.py"))

    for index, file_path in enumerate(python_files, start=1):
        source_code = file_path.read_text(encoding="utf-8")

        result = analyze_source(
            source_code,
            f"S{index:03d}",
        )

        results.append(result)

    return results
