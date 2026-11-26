from analyzer.similarity import compare_submissions, find_similar_pairs, find_similar_sources

def test_exact_match():
    code = "age = 15\nprint(age)"

    result = compare_submissions(code, code)

    assert result["match_type"] == "exact"


def test_normalized_match():
    code_a = "# Student A\nage = 15\nprint(age)"
    code_b = "# Student B\n\nage = 15\nprint(age)  "

    result = compare_submissions(code_a, code_b)

    assert result["match_type"] == "normalized"


def test_different_programs():
    code_a = "age = 15\nprint(age)"
    code_b = "age = 20\nprint(age)"

    result = compare_submissions(code_a, code_b)

    assert result["match_type"] == "different"


def test_indentation_is_significant():
    code_a = "if True:\n    print('Hello')"
    code_b = "if True:\n        print('Hello')"

    result = compare_submissions(code_a, code_b)

    assert result["match_type"] == "different"


def test_find_similar_pairs(tmp_path):
    # Create three synthetic submissions
    (tmp_path / "Anna_Smith.py").write_text(
        "# Student: Anna Smith\nage = 15\nprint(age)"
    )

    (tmp_path / "Ben_Jones.py").write_text(
        "# Student: Ben Jones\n\nage = 15\nprint(age)"
    )

    (tmp_path / "Cara_Liu.py").write_text(
        "age = 20\nprint(age)"
    )

    results = find_similar_pairs(tmp_path)

    # Only Anna and Ben should match
    assert len(results) == 1

    assert results[0] == {
        "submission_a": "S001",
        "submission_b": "S002",
        "match_type": "normalized",
    }

    # Student names must not appear in the results
    assert "Anna" not in str(results)
    assert "Ben" not in str(results)


def test_no_similar_pairs(tmp_path):
    (tmp_path / "student_001.py").write_text(
        "age = 15\nprint(age)"
    )

    (tmp_path / "student_002.py").write_text(
        "temperature = 32\nprint(temperature)"
    )

    results = find_similar_pairs(tmp_path)

    assert results == []

def test_find_similar_sources():
    submissions = [
        {
            "submission_id": "S001",
            "code": "score = 10\nprint(score)\n",
        },
        {
            "submission_id": "S002",
            "code": "# My solution\nscore = 10\nprint(score)\n",
        },
        {
            "submission_id": "S003",
            "code": "print('Hello world')\n",
        },
    ]

    matches = find_similar_sources(submissions)

    assert matches == [
        {
            "submission_a": "S001",
            "submission_b": "S002",
            "match_type": "normalized",
        }
    ]

def test_empty_submissions_are_not_similarity_matches():
    """Empty and comment-only files should not produce matches."""

    submissions = [
        {"submission_id": "S001", "code": ""},
        {"submission_id": "S002", "code": "\n  \n"},
        {"submission_id": "S003", "code": "# Just a comment\n"},
        {"submission_id": "S004", "code": "print('Hello')\n"},
    ]

    matches = find_similar_sources(submissions)

    assert matches == []
