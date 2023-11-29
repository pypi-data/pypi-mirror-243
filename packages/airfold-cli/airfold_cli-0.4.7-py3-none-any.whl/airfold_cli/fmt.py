import os
from enum import Enum
from pathlib import Path
from typing import Annotated, List, Optional

from airfold_common.format import ChFormat, Format
from airfold_common.project import (
    LocalFile,
    ProjectFile,
    dump_yaml,
    find_project_files,
    get_local_files,
    load_files,
)
from deepdiff import DeepDiff  # type: ignore
from rich.console import Console, ConsoleOptions, RenderResult
from rich.markup import escape
from rich.rule import Rule
from rich.syntax import Syntax
from typer import Context

from airfold_cli.error import AirfoldError
from airfold_cli.options import (
    DryRunOption,
    OverwriteFileOption,
    PathArgument,
    with_global_options,
)
from airfold_cli.prompts import prompt_overwrite_local_file, prompt_store_file
from airfold_cli.root import app, catch_airfold_error
from airfold_cli.utils import normalize_path_args


class FormatStatus(str, Enum):
    FIXED = "Fixed"
    REFORMATTED = "Reformatted"
    UNCHANGED = "Unchanged"


class FileHeader:
    def __init__(self, status: FormatStatus, file: LocalFile):
        self.file = file
        self.status = status
        if status == FormatStatus.FIXED:
            self.path_prefix = f"[bold green]{status.value} [/]"
        elif status == FormatStatus.REFORMATTED:
            self.path_prefix = f"[bold blue]{status.value} [/]"
        else:
            self.path_prefix = ""

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Rule(
            f"{self.path_prefix}[b]{escape(self.file.path)}[/]",
            style="border",
            characters="▁",
        )


class UnchangedFileBody:
    """Represents a file that was not changed."""

    def __init__(self, file: LocalFile):
        self.file = file

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Rule(characters="╲", style="hatched")
        yield Rule(" [blue]File was not changed ", characters="╲", style="hatched")
        yield Rule(characters="╲", style="hatched")
        yield Rule(style="border", characters="▔")


@app.command("fmt")
@catch_airfold_error()
@with_global_options
def fmt(
    ctx: Context,
    path: Annotated[Optional[List[str]], PathArgument] = None,
    dry_run: Annotated[bool, DryRunOption] = False,
    overwrite: Annotated[bool, OverwriteFileOption] = False,
) -> None:
    """Format local object files.
    \f

    Args:
        ctx: Typer context
        path: path to local object file(s)
        dry_run: print formatted files to stdout without saving them
        overwrite: overwrite existing files
    """
    app.apply_options(ctx)

    if not app.is_interactive() and not dry_run and not overwrite:
        raise AirfoldError("Use --overwrite in non-interactive mode")

    if dry_run and overwrite:
        app.print_warning("Warning: --dry-run and --overwrite are mutually exclusive, ignoring --overwrite")

    args = normalize_path_args(path)
    paths: list[Path] = find_project_files(args)
    files = load_files(paths)
    formatter: Format = ChFormat()

    for i, file in enumerate(files):
        normalized_data = formatter.normalize(file.data.copy(), file.name)
        kwargs: dict = file.dict(exclude={"data", "name"})
        normalized_file: LocalFile = (
            LocalFile(**kwargs, name=file.name, data=normalized_data)
            if isinstance(file, LocalFile)
            else get_local_files(formatter, [ProjectFile(**kwargs, name=file.name, data=normalized_data)])[0]
        )
        normalized_file.data.pop("name", None)
        ddiff = DeepDiff(file.data, normalized_file.data)
        format_status = FormatStatus.FIXED if ddiff else FormatStatus.UNCHANGED

        yaml_data: str = dump_yaml(normalized_file.data, remove_names=True)

        fpath = Path(normalized_file.path)
        if format_status == FormatStatus.UNCHANGED and fpath.exists():
            # TODO: store raw data in ProjectFile
            with open(fpath, "r") as original_file:
                raw_data = original_file.read()
                if raw_data != yaml_data:
                    format_status = FormatStatus.REFORMATTED

        app.console.print(FileHeader(format_status, normalized_file))

        if format_status == FormatStatus.UNCHANGED:
            app.console.print(UnchangedFileBody(normalized_file))
            continue
        else:
            app.console.print(Syntax(yaml_data, "yaml"))

        if dry_run:
            continue

        if not isinstance(file, LocalFile):
            default_path = os.path.join(os.getcwd(), normalized_file.path)
            fpath = (
                Path(prompt_store_file(default_path, console=app.console))
                if app.is_interactive()
                else Path(default_path)
            )
            os.makedirs(os.path.dirname(fpath), exist_ok=True)

        store: bool = True
        if fpath.exists() and not overwrite:
            store = prompt_overwrite_local_file(str(fpath), console=app.console)

        if not store:
            continue

        with open(fpath, "w") as yaml_file:
            yaml_file.write(yaml_data)
