import os
import shutil
from datetime import datetime
from .utils import parse_requirement


def compare_requirements_files(original_content: str, new_content: str) -> dict:
    """
    Compare two requirements.txt files to ensure package names match and @ directory
    specifications are removed appropriately.

    Args:
        original_content (str): Content of the original requirements.txt file
        new_content (str): Content of the new requirements.txt file

    Returns:
        dict: Dictionary containing comparison results and any discrepancies found
    """
    # Parse both files into dictionaries
    original_packages = {}
    new_packages = {}

    for line in original_content.split("\n"):
        name, version = parse_requirement(line)
        if name:
            original_packages[name] = {"version": version, "has_file_spec": "@" in line}

    for line in new_content.split("\n"):
        name, version = parse_requirement(line)
        if name:
            new_packages[name] = {"version": version, "has_file_spec": "@" in line}

    # Compare the files
    results = {
        "missing_in_new": [],
        "missing_in_original": [],
        "version_mismatches": [],
        "remaining_file_specs": [],
        "removed_file_specs": [],
        "total_packages": len(original_packages),
        "is_valid": True,
    }

    # Check for missing packages
    for package in original_packages:
        if package not in new_packages:
            results["missing_in_new"].append(package)
            results["is_valid"] = False

    for package in new_packages:
        if package not in original_packages:
            results["missing_in_original"].append(package)
            results["is_valid"] = False

    # Check versions and file specifications
    for package, original_info in original_packages.items():
        if package in new_packages:
            new_info = new_packages[package]

            # Check versions match
            if original_info["version"] != new_info["version"]:
                results["version_mismatches"].append(
                    {
                        "package": package,
                        "original_version": original_info["version"],
                        "new_version": new_info["version"],
                    }
                )
                results["is_valid"] = False

            # Check file specifications
            if original_info["has_file_spec"]:
                if new_info["has_file_spec"]:
                    results["remaining_file_specs"].append(package)
                    results["is_valid"] = False
                else:
                    results["removed_file_specs"].append(package)

    return results


def cleanup_old_backups(max_backups: int = 5):
    """
    Clean up old backups keeping only the specified number of most recent ones.

    Args:
        max_backups (int): Maximum number of backups to keep (default: 5)
    """
    backup_dir = os.path.join(os.getcwd(), "backups")

    try:
        if not os.path.exists(backup_dir):
            return

        # Get all backup files
        backups = []
        for f in os.listdir(backup_dir):
            if f.startswith("requirements_"):
                full_path = os.path.join(backup_dir, f)
                backups.append((f, os.path.getctime(full_path), full_path))

        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x[1], reverse=True)

        # Remove old backups
        if len(backups) > max_backups:
            for backup in backups[max_backups:]:
                os.remove(backup[2])
                print(f"Removed old backup: {backup[0]}")

    except Exception as e:
        print(f"Error during cleanup: {e}")


def print_comparison_results(results: dict):
    """Print the comparison results in a readable format."""
    print("\nRequirements Comparison Results:")
    print(f"Total packages analyzed: {results['total_packages']}")
    print(f"Valid transformation: {'Yes' if results['is_valid'] else 'No'}\n")

    if results["missing_in_new"]:
        print("Packages missing in new requirements:")
        for package in results["missing_in_new"]:
            print(f"  - {package}")

    if results["missing_in_original"]:
        print("\nNew packages not in original requirements:")
        for package in results["missing_in_original"]:
            print(f"  - {package}")

    if results["version_mismatches"]:
        print("\nVersion mismatches:")
        for mismatch in results["version_mismatches"]:
            print(
                f"  - {mismatch['package']}: {mismatch['original_version']} → {mismatch['new_version']}"
            )

    if results["remaining_file_specs"]:
        print("\nPackages still containing file specifications:")
        for package in results["remaining_file_specs"]:
            print(f"  - {package}")

    if results["removed_file_specs"]:
        print("\nPackages with file specifications correctly removed:")
        for package in results["removed_file_specs"]:
            print(f"  - {package}")


def handle_requirements_update(
    original_file: str, new_file: str, backup_suffix: str = ".bak"
):
    """
    Compare requirements files and handle the update process with user confirmation.
    Then clean up the temporary new requirements file.

    Args:
        original_file (str): Path to the original requirements.txt file
        new_file (str): Path to the new requirements.txt file
        backup_suffix (str): Suffix for backup file (default: '.bak')
    """
    try:
        # Create backups directory if it doesn't exist
        backup_dir = os.path.join(os.getcwd(), "backups")
        os.makedirs(backup_dir, exist_ok=True)

        # Read both files
        with open(original_file, "r") as f:
            original_content = f.read()
        with open(new_file, "r") as f:
            new_content = f.read()

        # Compare the files
        results = compare_requirements_files(original_content, new_content)
        print_comparison_results(results)

        # Ask for user confirmation
        while True:
            if not results["is_valid"]:
                print("\nWarning: Some discrepancies were found in the comparison.")

            response = input(
                "\nWould you like to update the original requirements.txt file? (yes/no): "
            ).lower()

            if response in ["yes", "y"]:
                # Create backup with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_filename = f"requirements_{timestamp}{backup_suffix}"
                backup_path = os.path.join(backup_dir, backup_filename)

                # Create backup
                shutil.copy2(original_file, backup_path)

                # Override original file with new content
                with open(original_file, "w") as f:
                    f.write(new_content)

                print(f"\nSuccess! Original file has been updated.")
                print(f"Backup created at: {backup_path}")

                # List all backups
                print("\nAvailable backups:")
                backups = sorted(
                    [f for f in os.listdir(backup_dir) if f.startswith("requirements_")]
                )
                for backup in backups:
                    backup_full_path = os.path.join(backup_dir, backup)
                    backup_size = os.path.getsize(backup_full_path)
                    backup_time = os.path.getctime(backup_full_path)
                    print(
                        f"  - {backup} ({backup_size} bytes, created: {datetime.fromtimestamp(backup_time).strftime('%Y-%m-%d %H:%M:%S')})"
                    )
                break

            elif response in ["no", "n"]:
                print("\nUpdate cancelled. No changes were made.")
                break

            else:
                print("\nPlease enter 'yes' or 'no'.")

        # Clean up the temporary new requirements file
        try:
            os.remove(new_file)
            print(f"\nCleaned up temporary file: {new_file}")
        except FileNotFoundError:
            print(f"\nNote: Temporary file {new_file} was already removed")
        except PermissionError:
            print(
                f"\nWarning: Could not remove temporary file {new_file} due to permissions"
            )

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e}")
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
