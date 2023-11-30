from typing import Annotated, List

from airfold_common.format import ChFormat, Format
from airfold_common.project import ProjectFile
from rich.syntax import Syntax
from rich.table import Table
from typer import Argument, Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.cli import AirfoldTyper
from airfold_cli.models import Config, OutputDataFormat
from airfold_cli.options import (
    DryRunOption,
    OutputDataFormatOption,
    with_global_options,
)
from airfold_cli.printer import print_plan
from airfold_cli.root import catch_airfold_error
from airfold_cli.utils import dump_json, load_config

pipe_app = AirfoldTyper(
    name="pipe",
    help="Pipe commands",
)

app.add_typer(pipe_app)


@pipe_app.command("delete")
@catch_airfold_error()
@with_global_options
def delete(
    ctx: Context,
    name: Annotated[str, Argument(help="Pipe name")],
    dry_run: Annotated[bool, DryRunOption] = False,
) -> None:
    """Delete pipe.
    \f

    Args:
        ctx: Typer context
        name: pipe name
        dry_run: show plan without executing it

    """
    pipe_app.apply_options(ctx)

    config: Config = load_config()
    api = AirfoldApi(config.key, config.endpoint)
    commands = api.project_pipe_delete(name=name, dry_run=dry_run)
    print_plan(commands, console=pipe_app.console)


@pipe_app.command("ls")
@catch_airfold_error()
@with_global_options
def ls(ctx: Context) -> None:
    """List pipes.
    \f

    Args:
        ctx: Typer context

    """
    pipe_app.apply_options(ctx)

    config: Config = load_config()
    api = AirfoldApi(config.key, config.endpoint)

    files = api.project_pull()

    formatter: Format = ChFormat()

    pipes: List[ProjectFile] = list(filter(lambda f: formatter.is_pipe(f.data), files))
    if not pipes:
        pipe_app.console.print("\t[magenta]NO PIPES[/magenta]")
        return

    table = Table(title="Pipes")
    table.add_column("Name", style="green", no_wrap=True)
    table.add_column("Description", no_wrap=True)

    for i, pipe in enumerate(pipes):
        table.add_row(str(pipe.name), str(pipe.data.get("description") or ""))

    pipe_app.console.print(table)


@pipe_app.command("data")
@catch_airfold_error()
@with_global_options
def data(
    ctx: Context,
    name: Annotated[str, Argument(help="Pipe name")],
    format: Annotated[OutputDataFormat, OutputDataFormatOption] = OutputDataFormat.NDJSON,
) -> None:
    """Get pipe data.
    \f

    Args:
        ctx: Typer context
        name: pipe name
        format: output data format

    """
    pipe_app.apply_options(ctx)

    config: Config = load_config()
    api = AirfoldApi(config.key, config.endpoint)
    jsons = api.project_pipe_get_data(name=name, format=format)

    for json_data in jsons:
        app.console.print(Syntax(dump_json(json_data), "json"))
