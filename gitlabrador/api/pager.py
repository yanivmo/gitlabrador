from typing import Any, Callable, Final

type Cursor = str
type HasNextPage = bool
type Page = [Any, Cursor, HasNextPage]

START_CURSOR: Final = ""


async def with_pagination(f: Callable[[Cursor], Page]):
    cursor = START_CURSOR
    has_next_page = True

    while has_next_page:
        [payload, cursor, has_next_page] = await f(cursor)
        yield payload
