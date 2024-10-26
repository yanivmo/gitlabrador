import click
from .groups import group, groups
from .config import config_group
from .tui import tui


@click.group()
def cli():
    """🐕 GitLab retriever for when naive solutions just won't cut"""
    pass


cli.add_command(config_group)
cli.add_command(group)
cli.add_command(groups)
cli.add_command(tui)
