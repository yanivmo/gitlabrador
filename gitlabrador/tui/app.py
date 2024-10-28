from textual.app import App

from gitlabrador.config import validate_settings
from .screens.welcome_screen import WelcomeScreen


class Tui(App):
    """GitLabrador textual user interface app."""

    TITLE = "🐕 GitLabrador"
    BINDINGS = [("q", "quit", "Quit")]
    CSS_PATH = ["css/global.tcss", "css/welcome_screen.tcss"]

    def __init__(self):
        super().__init__()
        validate_settings()
        self.dark = True

    def on_mount(self):
        self.push_screen(WelcomeScreen())
