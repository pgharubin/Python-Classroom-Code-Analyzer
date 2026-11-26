
from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_startup_message():
    """The app should prompt teachers to upload files."""

    app_path = Path(__file__).resolve().parent.parent / "app.py"
    app = AppTest.from_file(str(app_path)).run()

    assert len(app.exception) == 0
    assert len(app.info) == 1
    assert "Upload one or more Python files" in app.info[0].value


def test_no_results_before_upload():
    """The app should not display sample results automatically."""

    app_path = Path(__file__).resolve().parent.parent / "app.py"
    app = AppTest.from_file(str(app_path)).run()

    assert len(app.exception) == 0
    assert len(app.dataframe) == 0
    assert len(app.metric) == 0
