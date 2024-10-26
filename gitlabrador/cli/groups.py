import asyncio

import click
from rich import box
from rich.console import Console
from rich.table import Table

from gitlabrador.api import GitLabClient
from ..config import settings


async def groups_coroutine(parent_group):
    console = Console()
    table = Table(box=box.SIMPLE)

    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", no_wrap=True)
    table.add_column("Full Path", no_wrap=True)

    with console.status("Loading..."):
        gitlab = GitLabClient()
        async with gitlab.connect():
            async for group in gitlab.get_descendant_groups(parent_group):
                table.add_row(group.id, group.name, group.full_path)

    console.print(table)


@click.command()
@click.argument("parent_group", required=False)
def groups(parent_group):
    """
    List all descendant groups of PARENT_GROUP.

    If PARENT_GROUP not specified, will use the configured default-group.
    """
    if not parent_group:
        parent_group = settings.gitlab.default_group
    if not parent_group:
        raise click.UsageError(
            "PARENT_GROUP not specified and default-group not been set"
        )
    asyncio.run(groups_coroutine(parent_group))


@click.command()
@click.argument("group_name")
def group():
    """
    Perform operations on a specific group.
    """
    click.echo("Not implemented")
