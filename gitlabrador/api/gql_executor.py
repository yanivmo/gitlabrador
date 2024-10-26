from gql import gql
from gql.client import AsyncClientSession


class QueryExecutor:
    def __init__(self, session: AsyncClientSession):
        self.session = session

    async def execute(self, query: str) -> dict:
        return await self.session.execute(gql(query))
