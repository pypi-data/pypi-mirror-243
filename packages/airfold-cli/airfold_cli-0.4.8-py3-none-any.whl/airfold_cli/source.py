from typing import Annotated, List

from airfold_common.format import ChFormat, Format
from airfold_common.project import ProjectFile
from rich.table import Table
from typer import Argument, Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.cli import AirfoldTyper
from airfold_cli.models import Config
from airfold_cli.options import DryRunOption, with_global_options
from airfold_cli.printer import print_plan
from airfold_cli.root import catch_airfold_error
from airfold_cli.utils import load_config

source_app = AirfoldTyper(
    name="source",
    help="Source commands",
)

app.add_typer(source_app)


@source_app.command("delete")
@catch_airfold_error()
@with_global_options
def delete(
    ctx: Context,
    name: Annotated[str, Argument(help="Source name")],
    dry_run: Annotated[bool, DryRunOption] = False,
) -> None:
    """Delete source.
    \f

    Args:
        ctx: Typer context
        name: source name
        dry_run: show plan without executing it

    """
    source_app.apply_options(ctx)

    config: Config = load_config()
    api = AirfoldApi(config.key, config.endpoint)
    commands = api.project_source_delete(name=name, dry_run=dry_run)
    print_plan(commands, console=source_app.console)


@source_app.command("ls")
@catch_airfold_error()
@with_global_options
def ls(ctx: Context) -> None:
    """List sources.
    \f

    Args:
        ctx: Typer context

    """
    source_app.apply_options(ctx)

    config: Config = load_config()
    api = AirfoldApi(config.key, config.endpoint)

    files = api.project_pull()

    formatter: Format = ChFormat()

    sources: List[ProjectFile] = list(filter(lambda f: formatter.is_source(f.data), files))
    if not sources:
        source_app.console.print("\t[magenta]NO SOURCES[/magenta]")
        return

    table = Table(title="Sources")
    table.add_column("Name", style="green", no_wrap=True)
    table.add_column("Description", no_wrap=True)

    for i, source in enumerate(sources):
        table.add_row(str(source.name), str(source.data.get("description") or ""))

    source_app.console.print(table)
