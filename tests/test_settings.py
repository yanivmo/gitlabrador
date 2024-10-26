from black import datetime

from gitlabrador.config import settings, save_recent_project
from gitlabrador.models import Project


def test_recent_projects():
    # Start with empty list
    settings.app.recent_projects = []

    p = Project(
        id="gid://gitlab/Project/1",
        name="p1",
        name_with_namespace="booga / p1",
        description="P1",
        path="p1",
        full_path="booga/p1",
        web_url="https://gitlab.com/booga/p1",
    )
    save_recent_project(p)
    recent = settings.app.recent_projects

    assert len(recent) == 1
    assert recent[0][0] < datetime.now()
    assert recent[0][1] == p
