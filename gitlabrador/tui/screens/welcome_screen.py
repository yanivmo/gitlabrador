from rich.text import Text
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, OptionList
from textual.widgets.option_list import Option

from gitlabrador.config import settings
from .project_selection_screen import ProjectSelectionScreen


class WelcomeScreen(Screen):
    def compose(self):
        with Vertical(id="everything"):
            yield Header()
            with Vertical(id="content"):
                yield Label("Recent projects:", id="label-prompt")
                yield make_recent_projects_widget()
                with Center():
                    yield Button("All projects", id="button-all")
            yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        self.app.push_screen(ProjectSelectionScreen())


def make_recent_projects_widget():
    if not settings.app.recent_projects:
        return OptionList("No recent projects", disabled=True, id="recent-projects")
    else:
        projects = [
            Option(
                Text(p.name).append(f" ({p.name_with_namespace})", "gray69"),
                p.full_path,
            )
            for p in settings.app.recent_projects
        ]
        return OptionList(*projects, id="recent-projects")
