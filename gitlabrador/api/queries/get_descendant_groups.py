from typing import AsyncIterator

from gitlabrador.models import Group
from ..gql_executor import QueryExecutor
from ..pager import with_pagination, Page


def build_query(parent_group_full_path: str, cursor: str) -> str:
    return f"""
        query {{
          group(fullPath: "{parent_group_full_path}") {{
            descendantGroupsCount
            descendantGroups(includeParentDescendants: false, after: "{cursor}") {{
              nodes {{
                id
                name
                fullPath
              }}
              pageInfo {{
                hasNextPage
                endCursor
              }}
            }}
          }}
        }}"""


async def query_one_page(
    executor: QueryExecutor, parent_group_full_path: str, cursor: str
) -> Page:
    q = build_query(parent_group_full_path, cursor)
    result = await executor.execute(q)

    parent_group = result["group"]
    if not parent_group:
        return None, None, False

    descendants_dict = parent_group["descendantGroups"]
    descendants = [
        Group(
            id=g["id"],
            name=g["name"],
            full_path=g["fullPath"],
        )
        for g in descendants_dict["nodes"]
    ]
    page_info = descendants_dict["pageInfo"]
    return descendants, page_info["endCursor"], page_info["hasNextPage"]


async def query(
    executor: QueryExecutor, parent_group_full_path: str
) -> AsyncIterator[Group]:
    async def pager(cursor):
        return await query_one_page(executor, parent_group_full_path, cursor)

    async for page in with_pagination(pager):
        for group in page:
            yield group
