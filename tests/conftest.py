import os
import pytest
from pathlib import Path


@pytest.fixture
def sample_requirements():
    """Sample requirements content for testing."""
    return """
certifi @ file:///croot/certifi_1725551672989/work/certifi
numpy==1.26.4
pandas==2.2.3
python-dotenv @ file:///home/conda/feedstock_root/build_artifacts/python-dotenv-split_1706018097647/work
requests==2.32.3
"""


@pytest.fixture
def clean_requirements():
    """Clean requirements content without @ specifications."""
    return """
certifi
numpy==1.26.4
pandas==2.2.3
python-dotenv
requests==2.32.3
"""


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for file operations."""
    return tmp_path


@pytest.fixture
def requirements_file(temp_dir, sample_requirements):
    """Create a temporary requirements.txt file."""
    path = temp_dir / "requirements.txt"
    path.write_text(sample_requirements)
    return path


@pytest.fixture
def backup_dir(temp_dir):
    """Create a temporary backups directory."""
    path = temp_dir / "backups"
    path.mkdir()
    return path
