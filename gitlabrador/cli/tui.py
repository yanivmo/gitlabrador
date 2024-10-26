import click

from ..config import settings
from ..tui import Tui


@click.command()
def tui():
    """Run GitLabrador interactive textual user interface"""
    root_group = settings.gitlab.default_group
    if not root_group:
        raise click.UsageError(
            "default-group not been set. Use config command to set the value"
        )
    app = Tui()
    app.run(inline=True)
