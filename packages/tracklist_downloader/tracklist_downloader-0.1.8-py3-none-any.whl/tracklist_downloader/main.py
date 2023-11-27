import click
import importlib.metadata

from pathlib import Path

from tracklist_downloader.modules.config_validator import validate_config
from tracklist_downloader.modules.existing_download_checker import check_downloads
from tracklist_downloader.modules.downloader import download
from tracklist_downloader.modules.logging_module import setup_logger
from tracklist_downloader.modules.post_download_cleaner import post_download_cleanup

# Replace 'your_package_name' with the actual name of your package
package_name = 'tracklist-downloader'

try:
    version = importlib.metadata.version(package_name)
except importlib.metadata.PackageNotFoundError:
    version = 'unknown'


@click.command("main")
@click.version_option(version, prog_name="spotLy")
@click.argument(
    "path",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        path_type=Path
    ),
)
@click.option(
    "--validation-type",
    type=click.Choice(['hard', 'soft', 'none'], case_sensitive=False),
    default='hard',
    help="Specify the type of validation to perform."
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Perform a dry run without making actual changes."
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Run with debugger set to DEBUG"
)
@click.option(
    "--check-existing-downloads",
    is_flag=True,
    default=False, # TODO: set this to true once implemented
    help="Check existing"
)
def main(path: Path,
    validation_type: str,
    dry_run: bool,
    debug: bool,
    check_existing_downloads: bool
) -> None:
    """
    Main function to run the spotLy application.

    Args:
    - path (Path): Path to the configuration file.
    - validation_type (str): Type of validation to be performed ('hard', 'soft', or 'none').
    - dry_run (bool): If True, performs a dry run without making actual changes.
    - debug (bool): If True, runs with the debugger set to DEBUG.
    - check_existing_downloads (bool): If True, checks for existing downloads before proceeding.

    Returns:
    - None
    """
    logger = setup_logger(debug)
    config = validate_config(path, validation_type, logger)

    if check_existing_downloads:
        check_downloads()
    if not dry_run:
        download(config, logger)
    post_download_cleanup(config, logger)


if __name__ == "__main__":
    main()