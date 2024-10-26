from datetime import datetime
from pathlib import Path

from dynaconf import Dynaconf, loaders

from gitlabrador.models import Project

user_settings_path = str(Path.home() / ".gitlabrador.toml")

settings = Dynaconf(
    merge_enabled=True,
    settings_files=["settings.toml", ".secrets.toml", user_settings_path],
)

type RecentProject = [datetime, Project]


def save_recent_project(project: Project):
    recent: list[RecentProject] = settings.app.recent_projects
    recent = sorted(recent, key=lambda x: x[0])
    recent.append([datetime.now(), project])
    settings.app.recent_projects = recent


def save_user_settings():
    loaders.write(user_settings_path, settings.as_dict())


# Always refresh the user personal configuration file
save_user_settings()
