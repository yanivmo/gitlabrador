from datetime import datetime
from pathlib import Path

from dynaconf import Dynaconf, loaders

from gitlabrador.errors import GlbException
from gitlabrador.models import Project

DEFAULT_USER_SETTINGS_LOCATION = str(Path.home() / ".gitlabrador.yaml")

settings = Dynaconf(
    merge_enabled=True,
    core_loaders=["YAML"],
    settings_files=["settings.yaml", ".secrets.yaml", DEFAULT_USER_SETTINGS_LOCATION],
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
    if "gitlab" not in settings or "token" not in settings.gitlab:
        raise GlbException(
            "[white on red]Error: GitLab token not configured.[/]\n"
            + "Generate personal token at "
            + "[cyan]https://gitlab.com/-/user_settings/personal_access_tokens[/]\n"
            + "then configure using [cyan]gitlabrador config gitlab-token[/] command."
        )

    if len(settings.gitlab.token) < 10:
        raise GlbException(
            "[white on red]Error: Configured GitLab token is too short to be a real"
            + " token.[/]\nGenerate personal token at "
            + "[cyan]https://gitlab.com/-/user_settings/personal_access_tokens[/]\n"
            + "then configure using [cyan]gitlabrador config gitlab-token[/] command."
        )


def validate_gitlab_default_group():
    if "gitlab" not in settings or "default_group" not in settings.gitlab:
        raise GlbException(
            "[white on red]Error: GitLab default group not configured.[/]\n"
            + "Configure using [cyan]gitlabrador config default_group[/] command.",
        )

    if len(settings.gitlab.default_group) < 1:
        raise GlbException(
            "[white on red]Error: Configured GitLab default group "
            + f'[cyan]"{settings.gitlab.default_group}"[/] is too short.[/]\n'
            + "Configure using [cyan]gitlabrador config default_group[/] command."
        )


def validate_settings():
    validate_gitlab_token()
    validate_gitlab_default_group()


def save_user_settings():
    target = settings.get("override_user_settings", DEFAULT_USER_SETTINGS_LOCATION)
    loaders.write(target, settings.as_dict())


# Always refresh the user personal configuration file
save_user_settings()
