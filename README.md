
# Python Classroom Code Analyzer

## Version 1.0 — Classroom Submission Analysis

A Python-based tool designed to help Computer Science teachers review multiple student programming submissions efficiently.

Built with Python, Streamlit, and pytest.

## Features

- Upload multiple Python (.py) files.
- Check Python syntax without executing submitted code.
- Identify syntax errors and their line numbers.
- Analyze code structure using Python's Abstract Syntax Tree (AST).
- Count conditional branches, for loops, while loops, and functions.
- Flag possible email addresses and student IDs for privacy review.
- Identify exact and normalized code matches.
- Display results using pseudonymous submission identifiers.

## How to Run

Requirements: Python 3.10 or newer.

From the project directory, create a virtual environment:

    python3 -m venv .venv

Install dependencies:

    .venv/bin/python -m pip install -r requirements.txt

Start the application:

    .venv/bin/python -m streamlit run app.py

Open the local address displayed by Streamlit, typically:

    http://localhost:8501

Upload one or more Python files to begin analysis.

## Automated Testing

Run:

    .venv/bin/python -m pytest -v

Version 1.0 currently includes 36 passing automated tests.

## Privacy and Responsible Use

- Submitted Python code is parsed but never executed.
- No external AI service is used.
- When running locally, analysis takes place on the teacher's computer.
- Uploaded files are processed in memory.
- Analysis results use identifiers such as S001 and S002.
- Similarity findings require human interpretation and are not proof of plagiarism.

This prototype is intended for synthetic test submissions. Its limited privacy checks do not guarantee anonymization. Uploaded filenames may still contain identifying information, and other personal information may remain within source code.

Do not use real student records without appropriate institutional privacy and security review.

## Limitations

- Supports Python files only.
- Requires UTF-8 encoded files.
- Checks syntax and code structure, not program correctness.
- Does not execute or grade student programs.
- Similarity detection identifies exact matches or code differing only in comments and limited whitespace.
- Does not currently generate AI-powered feedback.
- Does not integrate with Google Classroom.
- Empty and comment-only submissions are excluded from similarity matching.
- A similarity match is not proof of plagiarism, and the absence
  of a match does not establish independent work.

## Intended Educational Benefit

The tool is designed to reduce the time teachers spend performing initial checks across a class of Python submissions.

Teachers remain responsible for interpreting findings, evaluating student understanding, and making assessment decisions.

## Future Development

Potential enhancements include secure code execution, teacher-reviewed AI feedback, and evaluation of feedback quality.
