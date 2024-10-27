import sys
from datetime import datetime
from pathlib import Path

from dynaconf import Dynaconf, loaders
from rich.console import Console

from gitlabrador.models import Project

DEFAULT_USER_SETTINGS_LOCATION = str(Path.home() / ".gitlabrador.toml")

settings = Dynaconf(
    merge_enabled=True,
    settings_files=["settings.toml", ".secrets.toml", DEFAULT_USER_SETTINGS_LOCATION],
)


def save_recent_project(project: Project):
    app_settings = settings.app
    recent: list = app_settings.recent_projects
    recent = sorted(recent, key=lambda x: x["timestamp"], reverse=True)

    new_item = {
        "timestamp": datetime.now().isoformat(),
        "project": project.to_dict(),
    }
    recent.insert(0, new_item)

    if len(recent) > settings.app.max_recent_projects:
        recent = recent[: settings.app.max_recent_projects]

    app_settings.recent_projects = recent
    settings.update({"app": app_settings})
    save_user_settings()


def validate_gitlab_token():
    console = Console()

    if "gitlab" not in settings or "token" not in settings.gitlab:
        console.print("\nError: GitLab token not configured.", style="white on red")
        console.print(
            "Generate personal token at [cyan]https://gitlab.com/-/user_settings/personal_access_tokens[/cyan]\n"
            + "then configure using [cyan]gitlabrador config gitlab-token[/cyan] command."
        )
        sys.exit(1)

    if len(settings.gitlab.token) < 10:
        console.print(
            "\nError: Configured GitLab token is too short to be a real token.",
            style="white on red",
        )
        console.print(
            "Generate personal token at [cyan]https://gitlab.com/-/user_settings/personal_access_tokens[/cyan]\n"
            + "then configure using [cyan]gitlabrador config gitlab-token[/cyan] command."
        )
        sys.exit(2)


def validate_settings():
    validate_gitlab_token()


def save_user_settings():
    target = settings.get("override_user_settings", DEFAULT_USER_SETTINGS_LOCATION)
    loaders.write(target, settings.as_dict())


# Always refresh the user personal configuration file
save_user_settings()
