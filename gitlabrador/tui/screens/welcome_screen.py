from rich.text import Text
from textual.containers import Center, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, OptionList
from textual.widgets.option_list import Option

from gitlabrador.banner import BANNER
from gitlabrador.config import settings
from .project_selection_screen import ProjectSelectionScreen


class WelcomeScreen(Screen):
    def __init__(self):
        super().__init__()
        self.recent_projects = OptionList(id="recent-projects")

    def compose(self):
        with Vertical(id="everything"):
            yield Header()
            with Horizontal():
                yield Label(BANNER, id="banner")
                with Vertical(id="content"):
                    yield Label("Recent projects:", id="label-prompt")
                    yield self.recent_projects
                    with Center():
                        yield Button("All projects", id="button-all")
            yield Footer()

    def on_screen_resume(self):
        self.refresh_recent_projects()

    def on_button_pressed(self, event: Button.Pressed):
        self.app.push_screen(ProjectSelectionScreen())

    def on_mount(self):
        self.refresh_recent_projects()

    def refresh_recent_projects(self):
        self.recent_projects.clear_options()

        if not settings.app.recent_projects:
            self.recent_projects.add_option(
                Option("No recent projects", id="placeholder")
            )
            self.recent_projects.disabled = True
        else:
            for access_time, proj in settings.app.recent_projects:
                text = Text(proj.name).append(
                    f" ({proj.name_with_namespace})", "gray69"
                )
                text.truncate(self.recent_projects.content_size.width)
                self.recent_projects.add_option(Option(text, proj.full_path))
            self.recent_projects.disabled = False

        return self.recent_projects


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
