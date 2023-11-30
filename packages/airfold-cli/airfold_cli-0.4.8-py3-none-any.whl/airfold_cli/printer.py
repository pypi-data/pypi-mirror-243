import logging
from typing import List, Optional

import rich
from airfold_common.log import log
from airfold_common.utils import grouped
from rich.panel import Panel

from airfold_cli.models import Command, CommandType


def print_plan(commands: List[Command], console: Optional[rich.console.Console] = None) -> None:
    console = console or rich.get_console()
    verbose = log.getEffectiveLevel() < logging.WARNING
    console.print("Execution plan:")
    if not commands:
        console.print("\t[magenta]NO CHANGES[/magenta]")
        return
    for i, cmd in enumerate(commands):
        name = ""
        new_name = ""
        type = ""
        command = ""
        if cmd.cmd in [CommandType.CREATE, CommandType.DELETE]:
            sources = [o for o in cmd.args if is_kind(o, "Source")]
            pipes = [o for o in cmd.args if is_kind(o, "PipeEntry")]
            if sources:
                source = sources[0]
                name = f'"{source.get("name")}"'
                type = source.get("type") or ""
                command = f"[cyan]{cmd.cmd}[/cyan]"
            elif pipes:
                name = f'"{pipes[0].get("name")}"'
                type = "pipe"
                command = f"[cyan]{cmd.cmd}[/cyan]"
        elif cmd.cmd == CommandType.RENAME:
            name = f"{cmd.args[0].get('name')}"
            if is_kind(cmd.args[0], "Source"):
                type = cmd.args[0].get("type") or ""
            elif is_kind(cmd.args[0], "PipeEntry"):
                type = "pipe"
            new_name = f"{cmd.args[1].get('name')}"
            command = f"[magenta]{cmd.cmd}[/magenta]"
        elif cmd.cmd == CommandType.REPLACE:
            type = "view"
            name = cmd.args[-1].get("id") or ""
            command = f"[magenta]{cmd.cmd}[/magenta]"
        elif cmd.cmd == CommandType.UPDATE:
            tables = [o for o in cmd.args if is_kind(o, "Table")]
            if tables:
                type = "table"
                name = f'"{tables[0].get("name")}"'
                command = f"[magenta]{cmd.cmd}[/magenta]"

        if cmd.cmd == CommandType.DELETE:
            command = f"[red]{cmd.cmd}[/red]"

        extended = ""
        if cmd.cmd == CommandType.RENAME:
            extended = f"[magenta]->[/magenta] [bold]{new_name}[/bold]"

        console.print(Panel(f"{i+1}\t{command}\t[yellow]{type}[/yellow] [bold]{name}[/bold] {extended}"))

        if verbose:
            if cmd.cmd == CommandType.RENAME:
                for j, (obj, obj_to) in enumerate(grouped(cmd.args, 2)):
                    console.print(
                        f"\t[bold]{obj.get('name') or obj.get('id')}[/bold]"
                        f" [magenta]->[/magenta] [bold]{obj_to.get('name') or obj_to.get('id')}[/bold]:\n"
                        f"\t{obj_to}"
                    )
                    console.print("")
            else:
                args = reversed(cmd.args) if cmd.cmd == CommandType.DELETE else cmd.args
                for j, obj in enumerate(args):
                    if is_kind(obj, "Node") or is_kind(obj, "Pipe"):
                        continue
                    console.print(f"\t{obj}")
            console.print("")


def is_kind(obj: dict, kind: str) -> bool:
    return obj.get("kind") == kind
