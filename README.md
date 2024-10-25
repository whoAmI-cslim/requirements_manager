# Requirements Manager

A Python package for managing requirements.txt files and their backups.
This will strip the @ file portion for any packages in the requirements.txt file. 
It will ask the user first if they want to strip these. If not, it will simply replicate 
running ```pip freeze > requirements.txt```

## Installation

```bash
pip install requirements-manager
```

## Usage

```python
from requirements_manager import handle_requirements_update, cleanup_old_backups

# Update requirements
handle_requirements_update('requirements.txt', 'new_requirements.txt')

# Clean up old backups
cleanup_old_backups(max_backups=5)
```

## CLI Usage

```bash
# Update requirements.txt or simply generate a new requirements.txt file.
reqmanager update

# Update requirements with optional flags
reqmanager update [--source <source_file>] [--destination <destination_file>]

# Clean up backups with optional flags
reqmanager cleanup --max-backups 5 [--backup-dir <backup_directory>]
```

# Clean up backups
```bash
reqmanager cleanup --max-backups 5
```
