from black import datetime

from gitlabrador.config import settings, save_recent_project
from gitlabrador.models import Project


def test_recent_projects(mocker, mocked_settings):
    mocker.patch("tests.test_settings.settings", new=mocked_settings)
    mocker.patch("gitlabrador.config.settings", new=mocked_settings)

    empty_recents = {"app": {"recent_projects": []}}
    settings.update(empty_recents, merge=True)
    assert settings.app.max_recent_projects > 0
    assert len(settings.app.recent_projects) == 0

    p = Project(
        id="gid://gitlab/Project/1",
        name="p1",
        name_with_namespace="booga / p1",
        description="P1",
        path="p1",
        full_path="booga/p1",
        web_url="https://gitlab.com/booga/p1",
    )

    max_recent_projects = settings.app.max_recent_projects
    for i in range(max_recent_projects):
        name = f"project{i}"
        p.name = name
        save_recent_project(p)

        recent = settings.app.recent_projects
        assert len(recent) == i + 1
        assert recent[0]["timestamp"] < datetime.now().isoformat()
        assert recent[0]["project"]["name"] == name, f"At position {i}"

    # Adding elements beyond max_recent_projects should pop the oldest element
    assert len(settings.app.recent_projects) == max_recent_projects
    latest_name = f"project{max_recent_projects}"
    p.name = latest_name
    save_recent_project(p)
    assert len(settings.app.recent_projects) == max_recent_projects
    assert settings.app.recent_projects[0]["project"]["name"] == latest_name
    assert settings.app.recent_projects[-1]["project"]["name"] == "project1"
