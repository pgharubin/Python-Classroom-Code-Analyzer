
from analyzer.privacy import strip_comments
from pathlib import Path
from itertools import combinations


def normalize_code(source_code: str) -> str:
    """Normalize code for similarity comparison."""

    try:
        code = strip_comments(source_code)
    except ValueError:
        # If tokenization fails, preserve the original code.
        # Syntax errors should not stop class analysis.
        code = source_code

    lines = [
        line.rstrip()
        for line in code.splitlines()
        if line.strip()
    ]

    return "\n".join(lines)


def compare_submissions(code_a: str, code_b: str) -> dict:
    """Compare two submissions, ignoring empty code."""

    normalized_a = normalize_code(code_a)
    normalized_b = normalize_code(code_b)

    # Empty or comment-only submissions are not useful matches.
    if not normalized_a or not normalized_b:
        match_type = "different"

    elif code_a == code_b:
        match_type = "exact"

    elif normalized_a == normalized_b:
        match_type = "normalized"

    else:
        match_type = "different"

    return {"match_type": match_type}

def find_similar_pairs(folder_path: str | Path) -> list[dict]:
    """Find matching Python submissions without exposing filenames."""

    folder = Path(folder_path)
    python_files = sorted(folder.glob("*.py"))

    submissions = []

    for index, file_path in enumerate(python_files, start=1):
        submissions.append({
            "submission_id": f"S{index:03d}",
            "code": file_path.read_text(encoding="utf-8"),
        })

    matches = []

    for submission_a, submission_b in combinations(submissions, 2):
        result = compare_submissions(
            submission_a["code"],
            submission_b["code"],
        )

        if result["match_type"] != "different":
            matches.append({
                "submission_a": submission_a["submission_id"],
                "submission_b": submission_b["submission_id"],
                "match_type": result["match_type"],
            })

    return matches

def find_similar_sources(submissions: list[dict]) -> list[dict]:
    """Compare submissions already loaded into memory."""

    matches = []

    for submission_a, submission_b in combinations(submissions, 2):
        result = compare_submissions(
            submission_a["code"],
            submission_b["code"],
        )

        if result["match_type"] != "different":
            matches.append({
                "submission_a": submission_a["submission_id"],
                "submission_b": submission_b["submission_id"],
                "match_type": result["match_type"],
            })

    return matches
