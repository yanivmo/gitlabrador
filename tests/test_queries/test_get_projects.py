import json
from unittest.mock import AsyncMock

import pytest

from gitlabrador.api import GitLabClient
from gitlabrador.api.gql_executor import QueryExecutor
from gitlabrador.models import Project


@pytest.mark.asyncio
async def test_one_page(mocker):
    mock_response = json.loads(
        """
        {
            "group": {
              "projects": {
                "nodes": [
                  {
                    "id": "gid://gitlab/Project/1",
                    "name": "p1",
                    "nameWithNamespace": "booga / p1",
                    "description": "P1",
                    "path": "p1",
                    "fullPath": "booga/p1",
                    "webUrl": "https://gitlab.com/booga/p1"
                  },
                  {
                    "id": "gid://gitlab/Project/2",
                    "name": "p2",
                    "nameWithNamespace": "booga / p2",
                    "description": "P2",
                    "path": "p2",
                    "fullPath": "booga/p2",
                    "webUrl": "https://gitlab.com/booga/p2"
                  },
                  {
                    "id": "gid://gitlab/Project/3",
                    "name": "p3",
                    "nameWithNamespace": "booga / p3",
                    "description": "P3",
                    "path": "p3",
                    "fullPath": "booga/p3",
                    "webUrl": "https://gitlab.com/booga/p3"
                  }
                ],
                "pageInfo": {
                  "endCursor": "xxx",
                  "hasNextPage": false
                }
              }
            }
        }"""
    )

    expected = [
        Project(
            id="gid://gitlab/Project/1",
            name="p1",
            name_with_namespace="booga / p1",
            description="P1",
            path="p1",
            full_path="booga/p1",
            web_url="https://gitlab.com/booga/p1",
        ),
        Project(
            id="gid://gitlab/Project/2",
            name="p2",
            name_with_namespace="booga / p2",
            description="P2",
            path="p2",
            full_path="booga/p2",
            web_url="https://gitlab.com/booga/p2",
        ),
        Project(
            id="gid://gitlab/Project/3",
            name="p3",
            name_with_namespace="booga / p3",
            description="P3",
            path="p3",
            full_path="booga/p3",
            web_url="https://gitlab.com/booga/p3",
        ),
    ]

    gitlab = GitLabClient()

    mock_execute = mocker.patch.object(
        QueryExecutor, "execute", AsyncMock(return_value=mock_response)
    )

    async with gitlab.connect():
        i = 0
        async for group in gitlab.get_projects("booga"):
            assert group == expected[i]
            i += 1

    assert 'group(fullPath: "booga")' in str(mock_execute.call_args.args[0])
