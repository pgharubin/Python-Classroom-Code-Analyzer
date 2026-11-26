import re
import io
import tokenize

def scan_for_emails(source_code: str) -> list[dict]:
    """Find possible email addresses without exposing their values."""

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    findings = []

    for line_number, line in enumerate(source_code.splitlines(), start=1):
        if re.search(pattern, line):
            findings.append({
                "line": line_number,
                "type": "possible_email",
            })

    return findings

def scan_for_student_ids(source_code: str) -> list[dict]:
    """Flag possible student IDs in explicitly named variables."""

    pattern = (
        r"\b(?:student_id|student_number|pupil_id)"
        r"\s*=\s*['\"]?\d{5,12}['\"]?"
    )

    findings = []

    for line_number, line in enumerate(source_code.splitlines(), start=1):
        if re.search(pattern, line, flags=re.IGNORECASE):
            findings.append({
                "line": line_number,
                "type": "possible_student_id",
            })

    return findings


def strip_comments(source_code: str) -> str:
    """Remove Python comments while preserving line numbers."""

    lines = source_code.splitlines(keepends=True)

    try:
        tokens = tokenize.generate_tokens(
            io.StringIO(source_code).readline
        )

        for token in tokens:
            if token.type == tokenize.COMMENT:
                row, start_col = token.start
                _, end_col = token.end

                line = lines[row - 1]

                lines[row - 1] = (
                    line[:start_col]
                    + " " * (end_col - start_col)
                    + line[end_col:]
                )

    except (tokenize.TokenError, IndentationError) as error:
        raise ValueError(
            "Unable to safely remove comments."
        ) from error

    return "".join(lines)

