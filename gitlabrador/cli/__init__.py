import click

from .config import config_group
from .groups import group, groups
from .tui import tui
from ..config import settings


@click.group()
def cli():
    """🐕 GitLab retriever for when naive solutions just won't cut"""
    if not settings.gitlab.token:
        raise click.UsageError(
            "GitLab access token has not been set. Use config command to set its value"
        )


cli.add_command(config_group)
cli.add_command(group)
cli.add_command(groups)
cli.add_command(tui)
