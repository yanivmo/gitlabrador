import json
from unittest.mock import AsyncMock

import pytest

from gitlabrador.api import GitLabClient
from gitlabrador.api.gql_executor import QueryExecutor
from gitlabrador.models import CurrentUser


@pytest.mark.asyncio
async def test_get_current_user(mocker):
    mock_response = json.loads(
        """
        {
            "currentUser": {
              "id": "gid://gitlab/User/2",
              "username": "enigo.montoya",
              "name": "Enigo Montoya"
            }
        }"""
    )
    expected = CurrentUser(
        id="gid://gitlab/User/2", name="Enigo Montoya", username="enigo.montoya"
    )

    gitlab = GitLabClient()

    mock_execute = mocker.patch.object(
        QueryExecutor, "execute", AsyncMock(return_value=mock_response)
    )

    async with gitlab.connect():
        group = await gitlab.get_current_user()
        assert expected == group

    assert "currentUser" in str(mock_execute.call_args.args[0])
