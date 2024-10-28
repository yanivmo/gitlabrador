import click

from ..tui import Tui


@click.command()
def tui():
    """Run GitLabrador interactive textual user interface"""
    app = Tui()
    app.run(inline=True)
