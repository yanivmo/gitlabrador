import pytest
from dynaconf import Dynaconf
from textual.widgets import OptionList

from gitlabrador.models import Project
from gitlabrador.tui import Tui


@pytest.fixture
def mocked_settings(mocker):
    settings = Dynaconf()
    settings.update(
        {
            "gitlab": {"default_group": {"name": "abc", "full_path": "path/to/abc"}},
            "app": {"recent_projects": []},
        }
    )
    return settings


@pytest.mark.asyncio
async def test_no_recent_projects(mocker, mocked_settings):
    mocker.patch("gitlabrador.tui.screens.welcome_screen.settings", new=mocked_settings)

    app = Tui()
    async with app.run_test() as pilot:
        # Wait for all the events to be handled
        await pilot.pause()

        recents_list: OptionList = app.get_widget_by_id("recent-projects", OptionList)
        assert recents_list is not None
        assert recents_list.is_disabled is True


@pytest.mark.asyncio
async def test_has_recent_projects(mocker, mocked_settings):
    recent_projects = [
        Project(
            id="gid://gitlab/Project/1",
            name="p1",
            name_with_namespace="booga / p1",
            description="P1",
            path="p1",
            full_path="booga/p1",
            web_url="https://gitlab.com/booga/p1",
        ).to_dict(),
        Project(
            id="gid://gitlab/Project/2",
            name="p2",
            name_with_namespace="booga / p2",
            description="P2",
            path="p2",
            full_path="booga/p2",
            web_url="https://gitlab.com/booga/p2",
        ).to_dict(),
        Project(
            id="gid://gitlab/Project/3",
            name="p3",
            name_with_namespace="booga / p3",
            description="P3",
            path="p3",
            full_path="booga/p3",
            web_url="https://gitlab.com/booga/p3",
        ).to_dict(),
    ]
    mocked_settings.app.recent_projects = recent_projects
    mocker.patch("gitlabrador.tui.screens.welcome_screen.settings", new=mocked_settings)

    app = Tui()
    async with app.run_test() as pilot:
        # Wait for all the events to be handled
        await pilot.pause()

        recents_list: OptionList = app.get_widget_by_id("recent-projects", OptionList)
        assert recents_list is not None
        assert recents_list.is_disabled is False
        assert recents_list.option_count == len(recent_projects)
        for i in range(recents_list.option_count):
            option = recents_list.get_option_at_index(i)
            assert option.id == recent_projects[i]["full_path"]
