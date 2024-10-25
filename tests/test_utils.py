import pytest
from src.requirements_manager.utils import (
    parse_requirement,
    create_new_lines,
    create_new_requirements,
)


@pytest.mark.parametrize(
    "input_line,expected",
    [
        ("pandas==2.2.3", ("pandas", "2.2.3")),
        ("certifi @ file:///path/to/file", ("certifi", None)),
        ("# comment", (None, None)),
        ("", (None, None)),
        ("requests", ("requests", None)),
    ],
)
def test_parse_requirement(input_line, expected):
    """Test requirement line parsing with various formats."""
    assert parse_requirement(input_line) == expected


def test_create_new_lines():
    """Test creation of new requirement lines."""
    input_lines = ["certifi @ file:///path/to/file\n", "pandas==2.2.3\n", "requests\n"]
    expected = ["certifi\n", "pandas==2.2.3\n", "requests\n"]
    assert create_new_lines(input_lines) == expected


def test_create_new_requirements(temp_dir):
    """Test creation of new requirements file."""
    # Create input file
    input_file = temp_dir / "requirements.txt"
    input_file.write_text("certifi @ file:///path/to/file\npandas==2.2.3")

    # Create output file
    output_file = temp_dir / "requirements_new.txt"
    create_new_requirements(str(input_file), str(output_file))

    # Verify output
    assert output_file.exists()
    content = output_file.read_text()
    assert "@" not in content
    assert "pandas==2.2.3" in content
