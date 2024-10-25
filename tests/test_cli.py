import pytest
from click.testing import CliRunner
from src.requirements_manager.cli import cli
import os


def test_update_command():
    """Test the update command in CLI."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create test files
        with open("requirements.txt", "w") as f:
            f.write("pandas==2.2.3\nnumpy==1.26.4")

        result = runner.invoke(cli, ["update"])
        assert result.exit_code == 0


def test_cleanup_command():
    """Test the cleanup command in CLI."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create backups directory and some files
        os.makedirs("backups")
        with open("backups/requirements_old.bak", "w") as f:
            f.write("test")

        result = runner.invoke(cli, ["cleanup", "--max-backups", "3"])
        assert result.exit_code == 0
