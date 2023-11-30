from typing import Annotated, Any, Callable, List, Optional

from merge_args import merge_args  # type: ignore
from pydantic import BaseModel, Extra
from typer import Argument, Option

from airfold_cli.models import OutputDataFormat, OverwriteType

GLOBAL_OPTIONS_PANEL_NAME = "Global options"

InteractivePromptOption: bool = Option(
    "--prompt", help="Force toggle prompts for this CLI run.", rich_help_panel=GLOBAL_OPTIONS_PANEL_NAME
)
"""If `True`, use interactive prompts in CLI commands. If `False`, no interactive
prompts will be used.
"""

VerbosityOption: Optional[int] = Option(
    "--verbose",
    "-v",
    help="Set verbosity level, can be repeated",
    count=True,
    rich_help_panel=GLOBAL_OPTIONS_PANEL_NAME,
)

PathArgument: Optional[List[str]] = Argument(file_okay=True, dir_okay=True, help="Path to a local object file(s)")

ApplyOption: bool = Option(
    "--apply",
    help="Apply the pushed pipeline, default is to plan only",
)

OverwriteOption: OverwriteType = Option(
    "--overwrite",
    help="When to overwrite existing objects",
)

OverwriteFileOption: bool = Option(
    "--overwrite",
    help="Overwrite existing local file(s) without confirmation",
)

DryRunOption: bool = Option(
    "--dry-run",
    help="Show execution plan without executing it",
)

TargetDir: Optional[str] = Argument(
    file_okay=False, dir_okay=True, help="Target directory to create files in, ('-' will dump to stdout)"
)

OutputPathArgument: str = Argument(file_okay=True, dir_okay=True, help="Output path")

OutputDataFormatOption: OutputDataFormat = Option(
    "--format",
    "-f",
    help="Output data format",
)


class GlobalOptions(BaseModel):
    verbose: Optional[int] = 0
    prompt: Optional[bool] = True

    def update_from_dict(self, d: dict[str, Any]):
        for k, v in d.items():
            if hasattr(self, k) and v is not None:
                setattr(self, k, v)

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow


def with_global_options(
    func: Callable,
) -> Callable:
    """Decorator to add global options to a command."""

    options = GlobalOptions()

    @merge_args(func)
    def wrapper(
        *args,
        # should be None by default to prevent overwriting config if an option was specified before a sub-command.
        prompt: Annotated[Optional[bool], InteractivePromptOption] = options.prompt,
        verbose: Annotated[Optional[int], VerbosityOption] = options.verbose,
        **kwargs,
    ):
        return func(*args, **kwargs)

    return wrapper
