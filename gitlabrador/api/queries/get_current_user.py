from gitlabrador.models import CurrentUser
from ..gql_executor import QueryExecutor


def build_query() -> str:
    return """
        query {{
          currentUser {{
            id
            username
            name
          }}
        }}"""


async def query(executor: QueryExecutor) -> CurrentUser:
    q = build_query()
    result = await executor.execute(q)

    current_user_dict = result["currentUser"]
    return CurrentUser(
        id=current_user_dict["id"],
        name=current_user_dict["name"],
        username=current_user_dict["username"],
    )
