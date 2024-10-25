import click
from . import core, utils


@click.group()
def cli():
    """Requirements Manager CLI tool"""
    pass


@cli.command()
@click.option(
    "--input-file", default="requirements.txt", help="Input requirements file"
)
@click.option(
    "--compare-file",
    default="requirements_new.txt",
    help="Comparison requirements file",
)
@click.option("--backup-suffix", default=".bak", help="Backup file suffix")
def update(input_file, compare_file, backup_suffix):
    """Update requirements file and manage backups"""
    utils.generate_requirements()
    utils.create_new_requirements(input_file, compare_file)
    core.handle_requirements_update(input_file, compare_file, backup_suffix)
    core.cleanup_old_backups(max_backups=5)


@cli.command()
@click.option("--max-backups", default=5, help="Maximum number of backups to keep")
def cleanup(max_backups):
    """Clean up old backup files"""
    core.cleanup_old_backups(max_backups)
