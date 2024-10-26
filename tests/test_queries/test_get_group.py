import json
from unittest.mock import AsyncMock

import pytest

from gitlabrador.api import GitLabClient
from gitlabrador.api.gql_executor import QueryExecutor
from gitlabrador.models import Group


@pytest.mark.asyncio
async def test_group_exists(mocker):
    mock_response = json.loads(
        """
        {
            "group": {
                "id": "gid://gitlab/Group/10",
                "name": "abc",
                "fullPath": "cba/abc"
            }
        }"""
    )
    expected = Group(id="gid://gitlab/Group/10", name="abc", full_path="cba/abc")

    gitlab = GitLabClient()

    mock_execute = mocker.patch.object(
        QueryExecutor, "execute", AsyncMock(return_value=mock_response)
    )

    async with gitlab.connect():
        group = await gitlab.get_group("cba/abc")
        assert expected == group

    assert 'group(fullPath: "cba/abc")' in str(mock_execute.call_args.args[0])


@pytest.mark.asyncio
async def test_group_missing(mocker):
    mock_response = json.loads("""{ "group": null }""")

    gitlab = GitLabClient()

    mock_execute = mocker.patch.object(
        QueryExecutor, "execute", AsyncMock(return_value=mock_response)
    )

    async with gitlab.connect():
        group = await gitlab.get_group("bad/group")
        assert group is None

    assert 'group(fullPath: "bad/group")' in str(mock_execute.call_args.args[0])
