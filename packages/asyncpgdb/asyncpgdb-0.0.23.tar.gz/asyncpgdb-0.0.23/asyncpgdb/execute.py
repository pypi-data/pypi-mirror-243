from abc import abstractmethod
from logging import Logger
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Coroutine,
    List,
    Iterable,
    Optional,
    Type,
)
from asyncpgdb.typing import T
from asyncpgdb.sql import get_query_args, get_command_args
from asyncpgdb.asyncpg import ConnectionAsyncpg as ConnAsyncpg

def _row_parser(
    __row_class: Type[T], attrs: Iterable[str] = ("model_validate", "parse_obj")
) -> Callable[..., T]:
    row_class_hasattr = lambda key: hasattr(__row_class, key)
    attr = next(filter(row_class_hasattr, attrs), None)
    return __row_class if attr is None else getattr(__row_class, attr)


async def _exec_query(query: str, vars: Optional[dict], func):
    return await func(*get_query_args(query=query, vars=vars))


async def fetch_var(
    query: str, vars: dict = None, conn: ConnAsyncpg = None, row_class: Type[T] = None
):
    var = await _exec_query(query=query, vars=vars, func=conn.fetchval)
    return (
        None
        if var is None
        else var
        if row_class is None
        else _row_parser(row_class or dict)(var)
    )


async def fetch_one(
    query: str, vars: dict = None, conn: ConnAsyncpg = None, row_class: Type[T] = None
) -> T:
    row = await _exec_query(query=query, vars=vars, func=conn.fetchrow)
    return row if row is None else _row_parser(row_class or dict)(dict(row))


async def fetch_all(
    query: str, vars: dict = None, conn: ConnAsyncpg = None, row_class: Type[T] = None
) -> List[T]:
    rows = await _exec_query(query=query, vars=vars, func=conn.fetch)
    if rows and isinstance(rows, list):
        parse_row = _row_parser(row_class or dict)
        result: List[row_class] = [parse_row(dict(row)) for row in rows]
    else:
        result = []

    return result


async def iter_all(
    query: str,
    vars: dict = None,
    conn: ConnAsyncpg = None,
    row_class: Type[T] = None,
) -> AsyncGenerator[T, Any]:
    async with conn.transaction():
        parse_row = _row_parser(row_class or dict)
        qa = get_query_args(query=query, vars=vars)
        async for row in conn.cursor(*qa):
            yield parse_row(dict(row))


async def execute(
    query: str, vars: dict = None, timeout: float = None, conn: ConnAsyncpg = None
):
    async with conn.transaction():
        qa = get_query_args(query=query, vars=vars)
        result = await conn.execute(*qa, timeout=timeout)
    return True if result is None else result


async def execute_many(
    query: str, vars_list: list[dict], timeout: float = None, conn: ConnAsyncpg = None
):
    async with conn.transaction():
        command_args = get_command_args(query=query, vars_list=vars_list)
        result = await conn.executemany(*command_args, timeout=timeout)
    return True if result is None else result


class ExecuteProtocol:
    @abstractmethod
    async def acquire_connection(self) -> ConnAsyncpg:
        pass

    @abstractmethod
    async def release(self, __conn: ConnAsyncpg):
        pass

    def log_info(self, *args):
        logger = getattr(self, "_logger", None)
        if logger is not None and isinstance(logger, Logger):
            logger.info(*args)

    async def _exec(self, method: Callable[..., Coroutine[Any, Any, T]], **kwargs):
        conn = await self.acquire_connection()
        kwargs["conn"] = conn
        result = await method(**kwargs)
        await self.release(conn)
        return result

    async def _iterate(self, method: Callable[..., Coroutine[Any, Any, T]], **kwargs):
        conn = await self.acquire_connection()
        kwargs["conn"] = conn
        async for obj in method(**kwargs):
            yield obj
        await self.release(conn)

    async def fetch_var(
        self, query: str, vars: dict = None, row_class: Type[T] = None
    ) -> T:
        return await self._exec(
            method=fetch_var, query=query, vars=vars, row_class=row_class
        )

    async def fetch_one(
        self, query: str, vars: dict = None, row_class: Type[T] = None
    ) -> T:
        return await self._exec(
            method=fetch_one, query=query, vars=vars, row_class=row_class
        )

    async def fetch_all(
        self, query: str, vars: dict = None, row_class: Type[T] = None
    ) -> List[T]:
        return await self._exec(
            method=fetch_all, query=query, vars=vars, row_class=row_class
        )

    async def iter_all(
        self, query: str, vars: dict = None, row_class: Type[T] = None
    ) -> AsyncGenerator[T, Any]:
        async for obj in self._iterate(
            method=iter_all, query=query, vars=vars, row_class=row_class
        ):
            yield obj

    async def execute(self, query: str, vars: dict = None, timeout: float = None):
        return await self._exec(method=execute, query=query, vars=vars, timeout=timeout)

    async def execute_many(
        self, query: str, vars_list: List[dict], timeout: float = None
    ):
        result = None
        if vars_list:
            result = await self._exec(
                method=execute_many, query=query, vars_list=vars_list, timeout=timeout
            )
        return result
