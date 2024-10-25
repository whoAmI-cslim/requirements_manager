import os


def parse_requirement(line: str) -> tuple:
    """Parse a requirement line into package name and version."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None, None

    # Handle lines with @ file: specifications
    if "@" in line:
        package_part = line.split("@")[0]
    else:
        package_part = line

    # Split into name and version
    if "==" in package_part:
        name, version = package_part.split("==", 1)
    else:
        name = package_part
        version = None

    return name.strip(), version.strip() if version else None


def create_new_lines(lines: list) -> list:
    """
    Creates new lines by removing version information from package lines.

    Args:
        lines (list): A list of lines from the requirements file.

    Returns:
        list: A list of lines with version information removed.
    """
    new_lines = []
    for line in lines:
        new_line = line.split("@")
        if len(new_line) > 1:
            new_line = new_line[0] + "\n"
        else:
            new_line = line
        new_lines.append(new_line)
    return new_lines


def generate_requirements():
    """Generates the current environment's requirements and writes them to 'requirements.txt'."""
    os.system("pip freeze > requirements.txt")


def create_new_requirements(input_file_name: str, compare_file_name: str):
    """
    Creates a new requirements file with version information removed.

    Args:
        input_file_name (str): The name of the input requirements file
        compare_file_name (str): The name of the new requirements file to be created
    """
    with open(input_file_name, "r") as f:
        lines = f.readlines()
    with open(compare_file_name, "w") as f:
        new_lines = create_new_lines(lines)
        f.writelines(new_lines)
