import pytest
import os
from datetime import datetime, timedelta
from src.requirements_manager.core import (
    compare_requirements_files,
    cleanup_old_backups,
    handle_requirements_update,
)


def test_compare_requirements_files_exact_match(sample_requirements):
    """Test comparison with identical files."""
    results = compare_requirements_files(sample_requirements, sample_requirements)
    assert results["is_valid"]
    assert len(results["missing_in_new"]) == 0
    assert len(results["missing_in_original"]) == 0
    assert len(results["version_mismatches"]) == 0


def test_compare_requirements_files_removed_specs(
    sample_requirements, clean_requirements
):
    """Test comparison when @ specifications are removed."""
    results = compare_requirements_files(sample_requirements, clean_requirements)
    assert results["is_valid"]
    assert "certifi" in results["removed_file_specs"]
    assert "python-dotenv" in results["removed_file_specs"]


def test_compare_requirements_files_version_mismatch():
    """Test comparison with version mismatches."""
    original = "pandas==2.2.3\nnumpy==1.26.4"
    new = "pandas==2.2.4\nnumpy==1.26.4"
    results = compare_requirements_files(original, new)
    assert not results["is_valid"]
    assert len(results["version_mismatches"]) == 1
    assert results["version_mismatches"][0]["package"] == "pandas"


def test_compare_requirements_files_missing_packages():
    """Test comparison with missing packages."""
    original = "pandas==2.2.3\nnumpy==1.26.4"
    new = "pandas==2.2.3"
    results = compare_requirements_files(original, new)
    assert not results["is_valid"]
    assert "numpy" in results["missing_in_new"]


def test_cleanup_old_backups(backup_dir):
    """Test backup cleanup functionality."""
    # Create test backup files with different timestamps
    for i in range(7):
        timestamp = datetime.now() - timedelta(days=i)
        backup_file = (
            backup_dir / f"requirements_{timestamp.strftime('%Y%m%d_%H%M%S')}.bak"
        )
        backup_file.touch()

    cleanup_old_backups(max_backups=5)
    remaining_files = list(backup_dir.glob("requirements_*.bak"))
    assert len(remaining_files) == 5


def test_handle_requirements_update(temp_dir, monkeypatch, capsys):
    """Test requirements update handling with user confirmation."""
    # Create test files
    original = temp_dir / "requirements.txt"
    original.write_text("pandas==2.2.3\nnumpy==1.26.4")
    new = temp_dir / "new_requirements.txt"
    new.write_text("pandas==2.2.3\nnumpy==1.26.4")

    # Mock user input
    monkeypatch.setattr("builtins.input", lambda _: "yes")

    # Run update
    handle_requirements_update(str(original), str(new))

    # Check output
    captured = capsys.readouterr()
    assert "Success!" in captured.out
    assert os.path.exists(temp_dir / "backups")


def test_handle_requirements_update_cancelled(temp_dir, monkeypatch, capsys):
    """Test requirements update handling when user cancels."""
    # Create test files
    original = temp_dir / "requirements.txt"
    original.write_text("pandas==2.2.3\nnumpy==1.26.4")
    new = temp_dir / "new_requirements.txt"
    new.write_text("pandas==2.2.3\nnumpy==1.26.4")

    # Mock user input
    monkeypatch.setattr("builtins.input", lambda _: "no")

    # Run update
    handle_requirements_update(str(original), str(new))

    # Check output
    captured = capsys.readouterr()
    assert "cancelled" in captured.out
