from textual.app import App

from .screens.welcome_screen import WelcomeScreen


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
