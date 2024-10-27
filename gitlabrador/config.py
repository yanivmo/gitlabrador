from datetime import datetime
from pathlib import Path

from dynaconf import Dynaconf, loaders

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


def save_user_settings():
    target = settings.get("override_user_settings", DEFAULT_USER_SETTINGS_LOCATION)
    loaders.write(target, settings.as_dict())


# Always refresh the user personal configuration file
save_user_settings()
