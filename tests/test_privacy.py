
from analyzer.privacy import (
    scan_for_emails,
    scan_for_student_ids,
    strip_comments,
)

def test_email_in_comment():
    code = "# Email: student@example.com\nprint('Hello')"
    result = scan_for_emails(code)

    assert len(result) == 1
    assert result[0]["line"] == 1
    assert result[0]["type"] == "possible_email"


def test_no_email():
    code = "age = 15\nprint(age)"
    result = scan_for_emails(code)

    assert result == []


def test_email_in_string():
    code = 'contact = "student@example.com"'
    result = scan_for_emails(code)

    assert len(result) == 1
    assert "student@example.com" not in str(result)


def test_student_id_detected():
    code = 'student_id = "12345678"'
    result = scan_for_student_ids(code)

    assert len(result) == 1
    assert result[0]["line"] == 1
    assert result[0]["type"] == "possible_student_id"


def test_ordinary_numbers_not_flagged():
    code = (
        "temperature = 12345678\n"
        "score = 95\n"
        "age = 15"
    )

    result = scan_for_student_ids(code)

    assert result == []


def test_student_number_not_exposed():
    code = "student_number = 87654321"
    result = scan_for_student_ids(code)

    assert len(result) == 1
    assert "87654321" not in str(result)


def test_remove_full_line_comments():
    code = "# Name: Emma Wilson\nage = 15"
    result = strip_comments(code)

    assert "Emma Wilson" not in result
    assert "age = 15" in result


def test_remove_inline_comments():
    code = "score = 90  # Student ID: 12345678"
    result = strip_comments(code)

    assert "score = 90" in result
    assert "12345678" not in result


def test_preserve_hash_in_strings():
    code = 'message = "Python uses # for comments"'
    result = strip_comments(code)

    assert result == code


def test_preserve_line_numbers():
    code = (
        "# Student name\n"
        "age = 15\n"
        "# Another comment\n"
        "print(age)"
    )

    result = strip_comments(code)

    assert len(result.splitlines()) == 4
    assert result.splitlines()[1] == "age = 15"
    assert result.splitlines()[3] == "print(age)"
