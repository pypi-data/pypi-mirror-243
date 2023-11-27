from abc import abstractmethod
from logging import Logger
from typing import Any, AsyncGenerator, Callable, Coroutine, List, Optional, Type
from asyncpgdb.typing import T
from asyncpgdb.sql import query_args
from asyncpgdb.asyncpg import ConnectionAsyncpg
from asyncpgdb.exception import handle_exception as __handle_exception

def _row_parser(__row_class: Type[T]) -> Callable[..., T]:
    return next(
        map(
            lambda key: getattr(__row_class, key),
            filter(
                lambda key: hasattr(__row_class, key), ("parse_obj", "model_validate")
            ),
        ),
        __row_class,
    )



def __exec__(func: Callable[..., Coroutine[Any, Any, T]]):
    exception_id = f"asyncpgdb.execute.{func.__name__}.exception"

    async def inner(*args, **kwargs) -> T:
        try:
            result = await func(*args, **kwargs)
        except Exception as exc:
            result = __handle_exception(exception_id, exc)
        return result

    return inner


def __iterate__(func):
    exception_id = f"asyncpgdb.iterate.{func.__name__}.exception"

    async def inner(*args, **kwargs):
        try:
            async for obj in func(*args, **kwargs):
                yield obj
        except Exception as exception:
            __handle_exception(exception_id, exception)

    return inner


async def _exec_query(query: str, vars: Optional[dict], func):
    qa = query_args(query=query, vars=vars)
    return await func(*qa.query_args())


@__exec__
async def fetch_var(
    query: str,
    vars: Optional[dict] = None,
    conn: ConnectionAsyncpg = None,
    row_class: Optional[Type[T]] = None,
):
    var = await _exec_query(query=query, vars=vars, func=conn.fetchval)
    return (
        None
        if var is None
        else var
        if row_class is None
        else _row_parser(row_class)(var)
    )


@__exec__
async def fetch_one(
    query: str,
    vars: Optional[dict] = None,
    conn: ConnectionAsyncpg = None,
    row_class: Type[T] = None,
) -> T:
    row = await _exec_query(query=query, vars=vars, func=conn.fetchrow)
    return (
        None
        if row is None
        else dict(row)
        if row_class is None
        else _row_parser(row_class)(row)
    )


@__exec__
async def fetch_all(
    query: str,
    vars: Optional[dict] = None,
    conn: ConnectionAsyncpg = None,
    row_class: Type[T] = None,
) -> List[T]:
    rows = await _exec_query(query=query, vars=vars, func=conn.fetch)
    if rows and isinstance(rows, list):
        row_parser = dict if row_class is None else row_parser(row_class)
        result: List[row_class] = list(map(row_parser, rows))
    else:
        result = []

    return result


@__iterate__
async def iter_all(
    query: str,
    vars: Optional[dict] = None,
    conn: ConnectionAsyncpg = None,
    row_class: Type[T] = None,
) -> AsyncGenerator[T,Any]:
    qa = query_args(query=query, vars=vars)
    async with conn.transaction():
        parse_row = dict if row_class is None else _row_parser(row_class)
        async for row in conn.cursor(*qa.query_args()):
            yield parse_row(row)


@__exec__
async def execute(
    query: str,
    vars: Optional[dict] = None,
    timeout: Optional[float] = None,
    conn: ConnectionAsyncpg = None,
):
    qa = query_args(query=query, vars=vars)
    result = True
    async with conn.transaction():
        result = await conn.execute(*qa.query_args(), timeout=timeout)
        if result is None:
            result = True
    return result


@__exec__
async def execute_many(
    query: str,
    vars_list: list[dict],
    timeout: Optional[float] = None,
    conn: ConnectionAsyncpg = None,
):
    result = None
    qa = query_args(command=query, vars_list=vars_list)

    async with conn.transaction():
        result = await conn.executemany(*qa.command_args(), timeout=timeout)
    if result is None:
        result = True
    return result


class ExecuteProtocol:
    @abstractmethod
    async def acquire_connection(self) -> ConnectionAsyncpg:
        pass

    @abstractmethod
    async def release(self, __conn: ConnectionAsyncpg):
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
        self,
        query: str,
        vars: Optional[dict] = None,
        row_class: Optional[Type[T]] = None,
    ):
        return await self._exec(
            method=fetch_var, query=query, vars=vars, row_class=row_class
        )

    async def fetch_one(
        self, query: str, vars: Optional[dict] = None, row_class: Type[T] = None
    ) -> T:
        return await self._exec(
            method=fetch_one, query=query, vars=vars, row_class=row_class
        )

    async def fetch_all(
        self, query: str, vars: Optional[dict] = None, row_class: Type[T] = None
    ) -> List[T]:
        return await self._exec(
            method=fetch_all, query=query, vars=vars, row_class=row_class
        )

    async def iter_all(
        self, query: str, vars: Optional[dict] = None, row_class: Type[T] = None
    ) -> AsyncGenerator[T, Any]:
        async for obj in self._iterate(
            method=iter_all, query=query, vars=vars, row_class=row_class
        ):
            yield obj

    async def execute(
        self,
        query: str,
        vars: Optional[dict] = None,
        timeout: Optional[float] = None,
    ):
        return await self._exec(method=execute, query=query, vars=vars, timeout=timeout)

    async def execute_many(
        self,
        query: str,
        vars_list: list[dict],
        timeout: Optional[float] = None,
    ):
        result = None
        if vars_list:
            result = await self._exec(
                method=execute_many,
                query=query,
                vars_list=vars_list,
                timeout=timeout,
            )
        return result
