from gitlabrador.models import Group
from ..gql_executor import QueryExecutor


def build_query(group_full_path: str) -> str:
    return f"""
        query {{
          group(fullPath: "{group_full_path}") {{
            id
            name
            fullPath
          }}
        }}"""


async def query(executor: QueryExecutor, group_full_path: str) -> Group | None:
    q = build_query(group_full_path)
    result = await executor.execute(q)

    group_dict = result["group"]
    if not group_dict:
        return None

    return Group(
        id=group_dict["id"], name=group_dict["name"], full_path=group_dict["fullPath"]
    )
