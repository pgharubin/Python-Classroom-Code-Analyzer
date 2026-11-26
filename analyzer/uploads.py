
from analyzer.batch import analyze_source
from analyzer.similarity import find_similar_sources


def analyze_uploads(uploaded_files):
    """Analyze uploaded Python submissions in memory."""

    submissions = []

    for index, uploaded_file in enumerate(uploaded_files, start=1):
        try:
            source_code = uploaded_file.getvalue().decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise ValueError(
                "Uploaded Python files must be UTF-8 encoded."
            ) from error

        submissions.append({
            "submission_id": f"S{index:03d}",
            "code": source_code,
        })

    results = [
        analyze_source(
            submission["code"],
            submission["submission_id"],
        )
        for submission in submissions
    ]

    similar_pairs = find_similar_sources(submissions)

    return results, similar_pairs
