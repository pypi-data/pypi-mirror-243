import typer
from prompt_toolkit import prompt
import rich
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.console import Console
from inferless_cli.utils.constants import DEFAULT_YAML_FILE_NAME
from inferless_cli.utils.helpers import (
    create_yaml,
    decrypt_tokens,
    is_inferless_yaml_present,
    yaml,
)

from inferless_cli.utils.services import get_volumes_list, create_volume


app = typer.Typer(
    no_args_is_help=True,
)

processing = "processing..."
desc = "[progress.description]{task.description}"
no_volumes = "[red]No volumes found in your account[/red]"


@app.command(
    "list",
    help="List all volumes.",
)
def list():
    _, _, _, workspace_id, _ = decrypt_tokens()
    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(description=processing, total=None)

        volumes = get_volumes_list(workspace_id)

        progress.remove_task(task_id)

    if len(volumes) == 0:
        rich.print(no_volumes)
        raise typer.Exit(1)

    table = Table(
        title="Volumes List",
        box=rich.box.ROUNDED,
        title_style="bold Black underline on white",
    )
    table.add_column("ID", style="yellow")
    table.add_column(
        "Name",
    )

    for volume in volumes:
        table.add_row(
            volume["id"],
            volume["name"],
        )

    console = Console()
    console.print(table)
    console.print("\n")


@app.command(
    "create",
    help="create volume.",
)
def list(
    name: str = typer.Option(None, "--name", "-n", help="Name of the volume"),
):
    _, _, _, workspace_id, workspace_name = decrypt_tokens()
    if name is None:
        name = prompt(
            "Enter the name for volume: ",
        )
    res = None
    with Progress(
        SpinnerColumn(),
        TextColumn(desc),
        transient=True,
    ) as progress:
        task_id = progress.add_task(
            description=f"Creating model in [blue]{workspace_name}[/blue] workspace",
            total=None,
        )
        res = create_volume(workspace_id, name)
        progress.remove_task(task_id)

    if "id" in res and "name" in res:
        rich.print(f"[green]Volume {res['name']} created successfully[/green]")
        is_yaml_present = is_inferless_yaml_present(DEFAULT_YAML_FILE_NAME)

        if is_yaml_present:
            is_update = typer.confirm(
                f"Found {DEFAULT_YAML_FILE_NAME} file. Do you want to update it? ",
                default=True,
            )
            if is_update == True:
                print("Updating yaml file")
                with open(DEFAULT_YAML_FILE_NAME, "r") as yaml_file:
                    config = yaml.load(yaml_file)
                    config["configuration"]["custom_volume_id"] = res["id"]
                    config["configuration"]["custom_volume_name"] = res["name"]
                    create_yaml(config, DEFAULT_YAML_FILE_NAME)
                    rich.print(
                        f"[green]{DEFAULT_YAML_FILE_NAME} file updated successfully[/green]"
                    )
