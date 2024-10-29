from rich.text import Text
from textual import work
from textual.containers import Center, Vertical, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, OptionList
from textual.widgets.option_list import Option

from gitlabrador.api import GitLabClient
from gitlabrador.banner import BANNER
from gitlabrador.config import settings
from .project_selection_screen import ProjectSelectionScreen


class WelcomeScreen(Screen):
    def __init__(self):
        super().__init__()
        self.recent_projects = OptionList(id="recent-projects")
        self.welcome_label = Label("Welcome", id="welcome-label")
        self.gitlab = GitLabClient()
        self.current_user = None

    def compose(self):
        yield Header()
        with Vertical(id="everything"):
            with Center():
                yield self.welcome_label
            with Center():
                with Horizontal():
                    yield Label(BANNER, id="banner")
                    with Vertical(id="content"):
                        yield Label("Recent projects:", id="label-prompt")
                        yield self.recent_projects
                        with Center():
                            yield Button("All projects", id="button-all")
        yield Footer()

    def on_mount(self):
        self.loading = True
        self.load_current_user()
        self.refresh_recent_projects()

    @work(exclusive=True)
    async def load_current_user(self):
        async with self.gitlab.connect():
            self.current_user = await self.gitlab.get_current_user()
        self.welcome_label.renderable = f"Welcome, {self.current_user.name}!"
        self.loading = False

    def on_screen_resume(self):
        self.refresh_recent_projects()

    def on_button_pressed(self, event: Button.Pressed):
        self.app.push_screen(ProjectSelectionScreen())

    def on_resize(self):
        self.refresh_recent_projects()

    def refresh_recent_projects(self):
        self.recent_projects.clear_options()

        if not settings.app.recent_projects:
            self.recent_projects.add_option(
                Option("No recent projects", id="placeholder")
            )
            self.recent_projects.disabled = True
        else:
            for item in settings.app.recent_projects:
                proj = item.project
                text = Text(str(proj.name)).append(
                    f" ({proj.name_with_namespace})", "gray69"
                )
                if self.recent_projects.content_size.width > 0:
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
