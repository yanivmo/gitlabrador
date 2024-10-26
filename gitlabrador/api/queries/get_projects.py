from typing import AsyncIterator

from gitlabrador.models import Project
from ..gql_executor import QueryExecutor
from ..pager import with_pagination, Page


def build_query(parent_group_full_path: str, cursor: str) -> str:
    return f"""
        query {{
          group(fullPath: "{parent_group_full_path}") {{
            projects(after: "{cursor}") {{
              nodes {{
                id
                name
                nameWithNamespace
                description
                path
                fullPath
                webUrl
              }}
              pageInfo {{
                endCursor
                hasNextPage
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

    projects_dict = parent_group["projects"]
    descendants = [
        Project(
            id=p["id"],
            name=p["name"],
            name_with_namespace=p["nameWithNamespace"],
            description=p["description"],
            path=p["path"],
            full_path=p["fullPath"],
            web_url=p["webUrl"],
        )
        for p in projects_dict["nodes"]
    ]
    page_info = projects_dict["pageInfo"]
    return descendants, page_info["endCursor"], page_info["hasNextPage"]


async def query(
    executor: QueryExecutor, parent_group_full_path: str
) -> AsyncIterator[Project]:
    async def pager(cursor):
        return await query_one_page(executor, parent_group_full_path, cursor)

    async for page in with_pagination(pager):
        for group in page:
            yield group
