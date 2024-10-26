import json
from unittest.mock import AsyncMock

import pytest

from gitlabrador.api import GitLabClient
from gitlabrador.api.gql_executor import QueryExecutor
from gitlabrador.models import Group


@pytest.mark.asyncio
async def test_one_page(mocker):
    mock_response = json.loads(
        """
    {
      "group": {
        "descendantGroupsCount": 4,
        "descendantGroups": {
          "nodes": [
            {
              "id": "gid://gitlab/Group/1","name":"Common","fullPath":"booga/common"
            },
            {
              "id": "gid://gitlab/Group/2", "name": "Infra", "fullPath": "booga/infra"
            },
            {
              "id":"gid://gitlab/Group/3","name": "Playg","fullPath": "booga/playgrnd"
            },
            {
              "id":"gid://gitlab/Group/4","name":"Services","fullPath":"booga/services"
            }
          ],
          "pageInfo": { "hasNextPage": false, "endCursor": "xxx" }
        }
      }
    }
    """
    )

    expected = [
        Group(id="gid://gitlab/Group/1", name="Common", full_path="booga/common"),
        Group(id="gid://gitlab/Group/2", name="Infra", full_path="booga/infra"),
        Group(id="gid://gitlab/Group/3", name="Playg", full_path="booga/playgrnd"),
        Group(id="gid://gitlab/Group/4", name="Services", full_path="booga/services"),
    ]

    gitlab = GitLabClient()

    mock_execute = mocker.patch.object(
        QueryExecutor, "execute", AsyncMock(return_value=mock_response)
    )

    async with gitlab.connect():
        i = 0
        async for group in gitlab.get_descendant_groups("booga"):
            assert group == expected[i]
            i += 1

    assert 'group(fullPath: "booga")' in str(mock_execute.call_args.args[0])
