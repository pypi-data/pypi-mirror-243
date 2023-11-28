from typer.testing import CliRunner

from lumaCLI.main import app
from lumaCLI.tests.utils import METADATA_DIR

runner = CliRunner()


def test_ingest(test_server):
    """
    Test if the 'ingest' command of the dbt module executes successfully.
    """
    result = runner.invoke(
        app,
        [
            "dbt",
            "ingest",
            "--metadata-dir",
            METADATA_DIR,
            "--luma-url",
            test_server,
        ],
    )

    assert result.exit_code == 0, result.output


def test_send_test_results(test_server):
    """
    Test if the 'send-test-results' command of the dbt module executes successfully.
    """
    result = runner.invoke(
        app,
        [
            "dbt",
            "send-test-results",
            "--metadata-dir",
            METADATA_DIR,
            "--luma-url",
            test_server,
        ],
    )
    assert result.exit_code == 0, result.output
