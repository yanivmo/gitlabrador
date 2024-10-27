import click

from .config import config_group
from .groups import group, groups
from .tui import tui


@click.group()
def cli():
    """🐕 GitLab retriever for when naive solutions just won't cut"""


cli.add_command(config_group)
cli.add_command(group)
cli.add_command(groups)
cli.add_command(tui)
