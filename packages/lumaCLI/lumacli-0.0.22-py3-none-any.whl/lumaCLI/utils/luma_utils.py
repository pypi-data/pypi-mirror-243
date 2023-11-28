import subprocess
from pathlib import Path
from typing import Optional, Union

import requests
import typer
import yaml
from rich import print
from rich.console import Console
from rich.panel import Panel
import json

from lumaCLI.models import Config, RequestInfo

# Create console for rich output
console = Console()

CONFIG_YAML_EXAMPLE = """# Example:
#
# groups:
#   - meta_key: "domain"
#     slug: "domains"
#     label_plural: "Domains"
#     label_singular: "Domain"
#     icon: "Cube"
#   - meta_key: "true_source"
#     slug: "sources"
#     label_plural: "Sources"
#     label_singular: "Source"
#     icon: "Cloud"
"""
OWNERS_YAML_EXAMPLE = """# Example:
#
# owners:
#   - email: "some@one.com"
#     first_name: "Dave"
#     last_name: "Smith"
#     title: "Director"
#   - email: "other@person.com"
#     first_name: "Michelle"
#     last_name: "Dunne"
#     title: "CTO"
#   - email: "someone@else.com"
#     first_name: "Dana"
#     last_name: "Pawlak"
#     title: "HR Manager"
"""




def json_to_dict(json_path: str) -> Optional[dict]:
    """
    Converts a JSON file to a Python dictionary.

    Args:
        json_path (str): The path to the JSON file.

    Returns:
        Optional[dict]: A dictionary representation of the JSON file, or None if an error occurs.
    """

    try:
        with open(json_path, "r") as json_file:
            # Load JSON data from file
            json_data: dict = json.load(json_file)
    except:
        json_data = None
    return json_data


def run_command(command: str, capture_output: bool = False) -> Optional[str]:
    """
    Execute a shell command and optionally capture its output.

    Args:
        command (str): The shell command to be executed.
        capture_output (bool, optional): Flag to determine if the command's output should be captured. Defaults to False.

    Returns:
        Optional[str]: The standard output of the command if `capture_output` is True, otherwise None.

    Raises:
        typer.Exit: Exits the script if the command execution fails.
    """

    try:
        if capture_output:
            result = subprocess.run(
                command, shell=True, check=True, capture_output=True, text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=True)
            return None
    except subprocess.CalledProcessError as e:
        console.print(
            Panel.fit(
                "[bold red]ERROR[/bold red]: An error occurred while running the command: [bold yellow]{}[/bold yellow]".format(
                    e
                ),
                title="Error",
                border_style="red",
            )
        )
        if e.output:
            console.print("[bold cyan]Output[/bold cyan]: {}".format(e.output))
        if e.stderr:
            console.print("[bold red]Error[/bold red]: {}".format(e.stderr))
    raise typer.Exit(1)


def print_response(response: requests.Response):
    """
    Print the details of an HTTP response in a formatted manner.

    Args:
        response (requests.Response): The HTTP response to be printed.
    """
    if response.ok:
        success_message = "[green]The request was successful!\nResponse:[/green]"
        print(Panel(success_message))
        try:
            print(response.json())
        except:
            print(Panel("[red]Error at printing items ingested[/red]"))
    else:
        try:
            error_message = f"[red]URL: {response.url}[/red]\n[red]An HTTP error occurred, response status code[/red]: {response.status_code} {response.json()['detail']}"
        except:
            error_message = f"[red]URL: {response.url}[/red]\n[red]An HTTP error occurred, response status code[/red]: {response.status_code} {response.text}"
        print(Panel(error_message))


def init_config(config_dir: Union[Path, str] = "./.luma", force: bool = False):
    """
    Initialize configuration files in the specified directory.

    Args:
        config_dir (Union[Path, str], optional): The directory where configuration files will be created. Defaults to "./.luma".
        force (bool, optional): If True, existing configuration files will be overwritten. Defaults to False.

    Raises:
        FileExistsError: If configuration files already exist and `force` is not set to True.
    """
    config_dir = Path(config_dir)

    config_path = config_dir / "config.yaml"
    owners_path = config_dir / "owners.yaml"

    if force:
        config_path.unlink(missing_ok=True)
        owners_path.unlink(missing_ok=True)
        try:
            config_dir.rmdir()
        except FileNotFoundError:
            pass

    if not config_path.exists() and not owners_path.exists():
        config_dir.mkdir(exist_ok=True)
        config_path.touch(exist_ok=False)
        owners_path.touch(exist_ok=False)
    else:
        raise FileExistsError

    config_path.write_text(CONFIG_YAML_EXAMPLE)
    owners_path.write_text(OWNERS_YAML_EXAMPLE)


def get_config(config_dir: Union[Path, str] = "./.luma") -> Optional[Config]:
    """
    Retrieve configuration data from YAML files in the specified directory.

    Args:
        config_dir (Union[Path, str], optional): The directory containing the configuration files. Defaults to "./.luma".

    Returns:
        Optional[Config]: The configuration object if the configuration is successfully loaded, otherwise None.

    Raises:
        FileNotFoundError: If the configuration files are missing.
        typer.Abort: If there is an error parsing the YAML files.
    """
    config_dir = Path(config_dir)

    config_path = config_dir / "config.yaml"
    owners_path = config_dir / "owners.yaml"

    config_missing = True
    config_empty = True
    owners_missing = True
    owners_empty = True

    config_dict = {}
    config_data = {}
    owners_data = {}

    if config_path.exists():
        config_missing = False
        with config_path.open("r") as f:
            try:
                config_data: Optional[dict] = yaml.safe_load(f)
                if config_data:
                    config_empty = False

            except yaml.YAMLError as exc:
                print("Error parsing YAML file: {}".format(exc))
                raise typer.Abort()

    if owners_path.exists():
        owners_missing = False
        with owners_path.open("r") as f:
            try:
                owners_data: Optional[dict] = yaml.safe_load(f)
                if owners_data:
                    owners_empty = False

            except yaml.YAMLError as exc:
                print("Error parsing YAML file: {}".format(exc))
                raise typer.Abort()

    if config_missing and owners_missing:
        raise FileNotFoundError

    if config_data is not None:
        config_dict.update(config_data)

    if owners_data is not None:
        config_dict.update(owners_data)

    return Config(**config_dict)


def send_config(config: Config, luma_url: str) -> requests.Response:
    """
    Send configuration data to a specified URL.

    Args:
        config (Config): The configuration data to be sent.
        luma_url (str): The URL where the configuration data will be sent.

    Returns:
        requests.Response: The response from the server after sending the configuration data.

    Raises:
        typer.Exit: If there is an error in sending the configuration data.
    """
    print(Panel(f"[yellow]Sending config info to luma[/yellow]"))

    try:
        response = requests.request(
            method="POST",
            url=f"{luma_url}/api/v1/config",
            json=config.dict(),
            verify=False,
            timeout=(
                3.05,
                60 * 30,
            ),
        )
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        error_message = "[red]The config request has failed. Please check your connection and try again."
        if isinstance(e, requests.exceptions.Timeout):
            error_message += " If you're using a VPN, ensure it's properly connected or try disabling it temporarily."
        elif isinstance(e, requests.exceptions.ConnectionError):
            error_message += (
                " This could be due to maximum retries being exceeded or failure to establish a new connection. "
                "Please check your network configuration."
            )
        print(Panel(error_message + "[/red]"))
        raise typer.Exit(1)

    if not response.ok:
        print(Panel(f"[red]Sending config info to luma FAILED[/red]"))

    print_response(response)
    return response


def perform_request(request_info: RequestInfo) -> requests.Response:
    """
    Send an HTTP request based on the provided request information.

    Args:
        request_info (RequestInfo):
        
    """
    print(Panel(f"[yellow]Sending request to luma[/yellow]"))
    try:
        response = requests.request(
            method=request_info.method,
            url=request_info.url,
            headers=request_info.headers,
            params=request_info.params,
            json=request_info.payload,
            verify=request_info.verify,
            timeout=request_info.timeout,
        )
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        error_messages = {
            requests.exceptions.Timeout: " If you're using a VPN, ensure it's properly connected or try disabling it temporarily.",
            requests.exceptions.ConnectionError: " This could be due to maximum retries being exceeded or failure to establish a new connection. Please check your network configuration.",
        }
        print(
            Panel(
                f"[red]The request has failed. Please check your connection and try again. {error_messages.get(type(e), '')}[/red]"
            )
        )
        raise typer.Exit(1)

    print_response(response)
    return response
