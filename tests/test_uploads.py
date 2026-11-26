
from io import BytesIO
from analyzer.uploads import analyze_uploads
import pytest

def test_analyze_uploads():
    # Simulate two uploaded Python files
    uploaded_files = [
        BytesIO(b"age = 15\nprint(age)\n"),
        BytesIO(b"# Example\nage = 15\nprint(age)\n"),
    ]

    results, similar_pairs = analyze_uploads(uploaded_files)

    # Both submissions should be analyzed
    assert len(results) == 2

    # Both should have valid Python syntax
    assert results[0]["valid"] is True
    assert results[1]["valid"] is True

    # Submissions receive anonymous identifiers
    assert results[0]["submission_id"] == "S001"
    assert results[1]["submission_id"] == "S002"

    # The code differs only by a comment
    assert similar_pairs == [
        {
            "submission_a": "S001",
            "submission_b": "S002",
            "match_type": "normalized",
        }
    ]

def test_rejects_invalid_encoding():
    """Reject Python files that are not UTF-8 encoded."""

    invalid_file = BytesIO(b"\xff\xfe\x00")

    with pytest.raises(ValueError, match="UTF-8"):
        analyze_uploads([invalid_file])

def test_malformed_submission_does_not_stop_batch():
    """One malformed submission must not stop class analysis."""

    uploaded_files = [
        BytesIO(b"print('hello')\n"),
        BytesIO(b"print('hi'\n"),
    ]

    results, similar_pairs = analyze_uploads(uploaded_files)

    assert len(results) == 2
    assert results[0]["valid"] is True
    assert results[1]["valid"] is False
    assert results[1]["line"] == 1
    assert similar_pairs == []
