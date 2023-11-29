from pathlib import Path
from typing import Annotated, List, Optional

import rich
from airfold_common.format import ChFormat, Format
from airfold_common.log import log
from airfold_common.project import (
    ProjectFile,
    dump_yaml,
    find_project_files,
    load_files,
)
from rich.console import Console
from typer import Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.error import AirfoldError
from airfold_cli.models import Config, OverwriteType
from airfold_cli.options import (
    DryRunOption,
    OverwriteOption,
    PathArgument,
    with_global_options,
)
from airfold_cli.printer import print_plan
from airfold_cli.root import catch_airfold_error
from airfold_cli.utils import load_config, normalize_path_args


@app.command("push")
@catch_airfold_error()
@with_global_options
def push(
    ctx: Context,
    path: Annotated[Optional[List[str]], PathArgument] = None,
    dry_run: Annotated[bool, DryRunOption] = False,
    overwrite: Annotated[OverwriteType, OverwriteOption] = OverwriteType.auto,
) -> None:
    """Push object(s) into runtime database.
    \f

    Args:
        ctx: Typer context
        path: path to local object file(s)
        dry_run: show execution plan without executing it
        overwrite: when to overwrite existing objects

    """
    app.apply_options(ctx)

    args = normalize_path_args(path)
    files: list[Path] = find_project_files(args)
    if not files:
        raise AirfoldError(f"Cannot find any project files in: {', '.join(args)}")
    log.info(f"Pushing files: {', '.join([str(f) for f in files])}")
    push_all(load_files(files), dry_run=dry_run, overwrite=overwrite, console=app.console)


def push_all(
    files: list[ProjectFile],
    config: Config | None = None,
    dry_run: bool = False,
    overwrite: OverwriteType = OverwriteType.auto,
    console: Optional[Console] = None,
) -> None:
    console = console or rich.get_console()
    conf: Config = config or load_config()
    api = AirfoldApi(conf.key, conf.endpoint)
    formatter: Format = ChFormat()

    commands = api.project_push(
        data=dump_yaml([formatter.normalize(file.data, file.name) for file in files]),
        dry_run=dry_run,
        overwrite=overwrite,
    )

    print_plan(commands, console=console)
