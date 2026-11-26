import streamlit as st
from analyzer.uploads import analyze_uploads

st.set_page_config(
    page_title="Python Classroom Code Analyzer",
    layout="wide",
)

st.title("Python Classroom Code Analyzer")
st.subheader("Version 1.0 — Classroom Submission Analysis")

st.write(
    "Analyze Python submissions for syntax errors, "
    "code structure, potential identifying information, "
    "and code similarity — without executing submitted code."
)
uploaded_files = st.file_uploader(
    "Upload Python submissions",
    type=["py"],
    accept_multiple_files=True,
    help="For testing, upload synthetic Python submissions only.",
)

if not uploaded_files:
    st.info(
        "Upload one or more Python files to begin analysis."
    )
    st.stop()

try:
    results, similar_pairs = analyze_uploads(uploaded_files)
except ValueError as error:
    st.error(str(error))
    st.stop()


# Display class summary
st.metric("Submissions Analyzed", len(results))


# Private reference for matching submission IDs to filenames
with st.expander(
    "Submission ID reference (private — do not screenshot)"
):
    filename_mapping = [
        {
            "Submission ID": f"S{index:03d}",
            "Uploaded filename": uploaded_file.name,
        }
        for index, uploaded_file in enumerate(
            uploaded_files, start=1
        )
    ]

    st.dataframe(
        filename_mapping,
        hide_index=True,
        width="stretch",
    )

st.subheader("Syntax & Privacy")

# Count submissions requiring privacy review
privacy_count = sum(
    result["privacy_review_required"]
    for result in results
)

if privacy_count > 0:
    st.warning(
        f"Privacy review required: {privacy_count} "
        f"submission(s) contain possible identifying information."
    )
else:
    st.success("No email addresses or student IDs detected "
               "by the current checks.")

# Display syntax and privacy results
syntax_columns = [
    "submission_id",
    "valid",
    "line",
    "message",
    "privacy_flags",
    "privacy_review_required",
]

syntax_results = [
    {column: result[column] for column in syntax_columns}
    for result in results
]

st.dataframe(syntax_results, hide_index=True, width="stretch")

# Display code structure results
st.subheader("Code Structure")

structure_columns = [
    "submission_id",
    "if_branches",
    "for_loops",
    "while_loops",
    "functions",
]

structure_results = [
    {column: result[column] for column in structure_columns}
    for result in results
]

st.dataframe(structure_results, hide_index=True, width="stretch")


# Analyze similarities between student submissions
st.subheader("Code Similarity Analysis")

st.metric("Similar Submission Pairs", len(similar_pairs))

if similar_pairs:
    st.dataframe(
        similar_pairs,
        hide_index=True,
        width="stretch",
    )
else:
    st.success("No exact or normalized matches detected.")

st.caption(
    "Similarity findings are for teacher review only. "
    "They are not evidence of plagiarism."
)

st.info(
    "Using synthetic submissions only. "
    "No student code is executed or sent to an AI service."
)
