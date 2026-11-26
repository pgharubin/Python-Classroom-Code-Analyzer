from analyzer.batch import analyze_folder, analyze_source

def test_analyze_folder(tmp_path):
    # Create two synthetic student submissions
    valid_file = tmp_path / "student_001.py"
    invalid_file = tmp_path / "student_002.py"

    valid_file.write_text("age = 15\nprint(age)")
    invalid_file.write_text("if age >= 13\n    print('Teen')")

    # Analyze both files
    results = analyze_folder(tmp_path)

    # Check that both submissions were processed
    assert len(results) == 2

    # Check the first submission
    assert results[0]["submission_id"] == "S001"
    assert results[0]["valid"] is True

    # Check the second submission
    assert results[1]["submission_id"] == "S002"
    assert results[1]["valid"] is False
    assert results[1]["line"] == 1

def test_batch_detects_email(tmp_path):
    code = (
        "# Contact: student@example.com\n"
        "age = 15\n"
        "print(age)"
    )

    file_path = tmp_path / "student_003.py"
    file_path.write_text(code, encoding="utf-8")

    results = analyze_folder(tmp_path)

    assert len(results) == 1
    assert results[0]["valid"] is True
    assert results[0]["privacy_flags"] == 1
    assert results[0]["privacy_review_required"] is True

    # The actual email must not appear in the results.
    assert "student@example.com" not in str(results)

def test_batch_analyzes_code_structure(tmp_path):
    code = """
temperature = 32

if temperature >= 35:
    print("Hot")
elif temperature >= 25:
    print("Warm")
else:
    print("Cool")
"""

    file_path = tmp_path / "student_001.py"
    file_path.write_text(code, encoding="utf-8")

    results = analyze_folder(tmp_path)

    assert len(results) == 1
    assert results[0]["valid"] is True
    assert results[0]["if_branches"] == 2
    assert results[0]["for_loops"] == 0
    assert results[0]["while_loops"] == 0
    assert results[0]["functions"] == 0

def test_analyze_source():
    code = """
# Synthetic student submission
student_id = "12345678"
email = "student@example.com"

age = 15

if age >= 13:
    print("Teenager")
"""

    result = analyze_source(code, "S001")

    # Verify submission identification
    assert result["submission_id"] == "S001"

    # Verify syntax analysis
    assert result["valid"] is True

    # Verify privacy screening
    assert result["privacy_flags"] == 2
    assert result["privacy_review_required"] is True

    # Verify code structure
    assert result["if_branches"] == 1
    assert result["for_loops"] == 0

    # Identifying information must not appear in results
    assert "12345678" not in str(result)
    assert "student@example.com" not in str(result)
