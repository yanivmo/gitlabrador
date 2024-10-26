import asyncio

from rich.style import Style
from rich.text import Text
from textual import work
from textual.app import App
from textual.widgets import OptionList, Tree
from textual.widgets.tree import TreeNode

from .screens.welcome_screen import WelcomeScreen
from ..api import GitLabClient
from ..config import settings
from ..models import Group


class Tui(App):
    """GitLabrador textual user interface app."""

    TITLE = "🐕 GitLabrador"
    BINDINGS = [("q", "quit", "Quit"), ("d", "toggle_dark", "Toggle dark/light")]
    CSS_PATH = ["css/global.tcss", "css/welcome_screen.tcss"]

    def __init__(self):
        super().__init__()
        self.dark = True

    def on_mount(self):
        self.push_screen(WelcomeScreen())

    def action_toggle_dark(self) -> None:
        """Toggle dark to light mode and back."""
        self.dark = not self.dark

