"""
This module implements a command-line interface (CLI) for the Luma application.
It provides commands for database operations, configuration management, and other utilities.
"""

import importlib.metadata

# Standard library imports
import urllib3

# Third-party library imports
import typer
from rich.panel import Panel

# Local module imports
import lumaCLI.commands.config as config
import lumaCLI.commands.dbt as dbt
import lumaCLI.commands.postgres as postgres
from lumaCLI.utils.options import CLI_NAME

__version__ = importlib.metadata.version(__package__ or __name__)

# Disable warnings related to insecure requests for specific cases
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Create a Typer application with configured properties
app = typer.Typer(
    name=CLI_NAME,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=True,
    pretty_exceptions_short=True,
)

def print_did_you_mean_luma():
    """Prints a suggestion panel if 'lumaCLI' is mistakenly used."""
    print(
        Panel(
            f"Whoops, you typed [bold red]lumaCLI[/bold red], did you mean '[bold green]luma[/bold green]' ??",
            border_style="blue",
        )
    )

def version_callback(show_version: bool):
    """
    Prints the version of the application and exits.
    
    Args:
        show_version (bool): If True, shows the version.
    """
    if show_version:
        typer.echo(__version__)
        raise typer.Exit()

@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
):
    """
    Main function for the Typer application.
    
    Args:
        version (bool): Flag to show the version and exit.
    """
    pass

# Add commands to the Typer application
app.add_typer(dbt.app, name="dbt")
app.add_typer(postgres.app, name="postgres")
app.add_typer(config.app, name="config")
