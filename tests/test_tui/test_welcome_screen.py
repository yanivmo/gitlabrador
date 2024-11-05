import pytest
from textual.widgets import OptionList

from gitlabrador.models import Project, CurrentUser
from gitlabrador.tui import Tui
from gitlabrador.tui.screens.welcome_screen import WelcomeScreen


@pytest.fixture
def tui() -> Tui:
    return Tui(WelcomeScreen())


@pytest.fixture
def user(mocker) -> CurrentUser:
    api = mocker.patch(
        "gitlabrador.tui.screens.welcome_screen.GitLabClient", autospec=True
    )
    user = CurrentUser(id="U1", username="user", name="User")
    api.get_current_user.return_value = user
    return user


@pytest.mark.asyncio
async def test_screen_no_recent_projects(user, tui, mocker, mocked_settings):
    mocker.patch("gitlabrador.tui.screens.welcome_screen.settings", new=mocked_settings)

    async with tui.run_test() as pilot:
        # Wait for all the events to be handled
        await pilot.pause()

        recents_list: OptionList = tui.get_widget_by_id("recent-projects", OptionList)
        assert recents_list is not None
        assert recents_list.is_disabled is True


@pytest.mark.asyncio
async def test_screen_has_recent_projects(user, tui, mocker, mocked_settings):
    recent_projects = [
        {
            "timestamp": "2024-10-26T09:12:08.041492",
            "project": Project(
                id="gid://gitlab/Project/1",
                name="p1",
                name_with_namespace="booga / p1",
                description="P1",
                path="p1",
                full_path="booga/p1",
                web_url="https://gitlab.com/booga/p1",
            ).to_dict(),
        },
        {
            "timestamp": "2024-10-26T09:12:07.041492",
            "project": Project(
                id="gid://gitlab/Project/2",
                name="p2",
                name_with_namespace="booga / p2",
                description="P2",
                path="p2",
                full_path="booga/p2",
                web_url="https://gitlab.com/booga/p2",
            ).to_dict(),
        },
        {
            "timestamp": "2024-10-26T09:12:06.041492",
            "project": Project(
                id="gid://gitlab/Project/3",
                name="p3",
                name_with_namespace="booga / p3",
                description="P3",
                path="p3",
                full_path="booga/p3",
                web_url="https://gitlab.com/booga/p3",
            ).to_dict(),
        },
    ]
    mocked_settings.update({"app": {"recent_projects": recent_projects}}, merge=True)
    mocker.patch("gitlabrador.tui.screens.welcome_screen.settings", new=mocked_settings)

    async with tui.run_test() as pilot:
        # Wait for all the events to be handled
        await pilot.pause()

        recents_list: OptionList = tui.get_widget_by_id("recent-projects", OptionList)
        assert recents_list is not None
        assert recents_list.is_disabled is False
        assert recents_list.option_count == len(recent_projects)
        for i in range(recents_list.option_count):
            option = recents_list.get_option_at_index(i)
            assert option.id == recent_projects[i]["project"]["full_path"]

            assert str(option.prompt).startswith(
                recent_projects[i]["project"]["name"]
            ), (
                f"{i}: '{option.prompt}' not starting with "
                + f"'{recent_projects[i]["project"]["name"]}'"
            )
