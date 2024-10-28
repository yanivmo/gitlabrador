import asyncio

import click
from rich.console import Console
from rich.text import Text

from gitlabrador.api import GitLabClient
from gitlabrador.config import (
    settings,
    save_user_settings,
    validate_gitlab_default_group,
)


@click.group(name="config")
def config_group():
    """
    Manage GitLabrador configuration.
    """


async def set_default_group_coroutine(group_full_path):
    with Console().status("Retrieving group details from GitLab.."):
        gitlab = GitLabClient()
        async with gitlab.connect():
            group = await gitlab.get_group(group_full_path)
            if not group:
                raise click.UsageError(
                    f"Failed to retrieve the group {group_full_path}"
                )
        settings.gitlab.default_group = group.to_dict()
        save_user_settings()


def keyValue(key: str, value) -> Text:
    return (
        Text(key, style="bright_blue").append(" ").append(value, style="bright_green")
    )


@config_group.command()
@click.argument("group_full_path", required=False)
def default_group(group_full_path):
    """
    Read or set GitLabrador's default GitLab project group.

    If GROUP_FULL_NAME not specified, will print the current value.
    Will exit with an error if the value has not been set yet.
    """
    if group_full_path:
        asyncio.run(set_default_group_coroutine(group_full_path))
    else:
        validate_gitlab_default_group()
        group = settings.gitlab.default_group

        text = Text("default-group:", style="bright_magenta")
        text.append("\n  ").append_text(keyValue("id:      ", group.id))
        text.append("\n  ").append_text(keyValue("name:    ", group.name))
        text.append("\n  ").append_text(keyValue("fullPath:", group.full_path))
        Console().print(text)


@config_group.command()
def gitlab_token():
    """
    Set GitLab access token.

    Prompts user to enter the token interactively.

    Generate tokens via GitLab user settings page:
    https://gitlab.com/-/user_settings/personal_access_tokens
    """
    token = click.prompt("Enter GitLab access token", hide_input=True)
    settings.gitlab.token = token
    save_user_settings()
