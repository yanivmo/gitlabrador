from contextlib import asynccontextmanager
from typing import Final, AsyncIterator

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport

from .gql_executor import QueryExecutor
from .queries import get_group, get_descendant_groups, get_projects
from ..config import settings, validate_gitlab_token
from ..models import Group, Project

REQUEST_TIMEOUT_SECONDS: Final = 60

LIST_START_CURSOR: Final = ""


class GitLabClient:
    def __init__(self):
        validate_gitlab_token()

        transport = AIOHTTPTransport(
            url=settings.gitlab.graphql_url,
            headers={"Authorization": f"Bearer {settings.gitlab.token}"},
        )

        self.graphql = Client(
            transport=transport, execute_timeout=REQUEST_TIMEOUT_SECONDS
        )
        self.session = None

    @asynccontextmanager
    async def connect(self):
        async with self.graphql as session:
            self.session = session
            yield

    async def get_group(self, group_full_path: str) -> Group | None:
        return await get_group.query(QueryExecutor(self.session), group_full_path)

    async def get_descendant_groups(
        self, parent_group_full_path: str
    ) -> AsyncIterator[Group]:
        async for group in get_descendant_groups.query(
            QueryExecutor(self.session), parent_group_full_path
        ):
            yield group

    async def get_projects(self, parent_group_full_path: str) -> AsyncIterator[Project]:
        async for project in get_projects.query(
            QueryExecutor(self.session), parent_group_full_path
        ):
            yield project
