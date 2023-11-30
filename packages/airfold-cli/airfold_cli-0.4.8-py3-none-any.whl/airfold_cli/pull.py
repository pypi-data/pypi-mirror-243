import os
from typing import Annotated, Optional

from airfold_common.format import ChFormat, Format
from airfold_common.project import (
    LocalFile,
    dump_project_files,
    dump_yaml,
    get_local_files,
)
from rich.syntax import Syntax
from typer import Context

from airfold_cli import app
from airfold_cli.api import AirfoldApi
from airfold_cli.error import AirfoldError
from airfold_cli.models import Config
from airfold_cli.options import TargetDir, with_global_options
from airfold_cli.root import catch_airfold_error
from airfold_cli.utils import PROJECT_DIR, load_config


def pull_all(config: Config | None = None) -> list[LocalFile]:
    api = AirfoldApi.from_config(config or load_config())
    formatter: Format = ChFormat()
    files = api.project_pull()
    return get_local_files(formatter, files)


@app.command("pull")
@catch_airfold_error()
@with_global_options
def pull(
    ctx: Context,
    path: Annotated[Optional[str], TargetDir] = None,
):
    """Pull objects from the runtime database.
    \f

    Args:
        ctx: Typer context
        path: optional directory to pull into ('-' will dump objects to stdout)
    """
    app.apply_options(ctx)

    if not path:
        path = os.path.join(os.getcwd(), PROJECT_DIR)
    if path != "-":
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.isdir(path):
            raise AirfoldError(f"Target path is not a directory: {path}")
    files = pull_all()
    if path == "-":
        app.console.print(Syntax(dump_yaml([file.data for file in files]), "yaml"))
    else:
        dump_project_files(files, path)
