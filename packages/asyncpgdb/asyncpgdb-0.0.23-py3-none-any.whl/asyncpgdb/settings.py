from typing import Any, Optional, Type
from asyncpgdb.asyncpg import ConnectionAsyncpg
from pydantic import BaseModel
from .util import getter_dict, getter_validate


class SettingsBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    def connect_kwargs(self, exclude_unset: bool = True, exclude_none: bool = True):
        connect_kwargs = getter_dict(self.__class__)(
            self, exclude_unset=exclude_unset, exclude_none=exclude_none
        )
        result = lambda: connect_kwargs
        return result


class ConnectionSettings(SettingsBaseModel):
    dsn: Optional[str]
    host: Optional[str]
    port: Optional[str]
    user: Optional[str]
    password: Optional[str]
    passfile: Optional[str]
    database: Optional[str]
    loop: Optional[Any]
    timeout: Optional[float]
    statement_cache_size: Optional[int]
    max_cached_statement_lifetime: Optional[float]
    max_cacheable_statement_size: Optional[int]
    command_timeout: Optional[float]
    ssl: Optional[str]
    direct_tls: bool
    connection_class: Type[ConnectionAsyncpg]
    record_class: Optional[Type]
    server_settings: Optional[dict]


class DatabaseSettings(SettingsBaseModel):
    dsn: str
    min_size: int
    max_size: int
    max_queries: int
    command_timeout: int
    max_inactive_connection_lifetime: float
    setup: Optional[Any]
    init: Optional[Any]
    loop: Optional[Any]
    ssl: Optional[str]
    connection_class: Type[ConnectionAsyncpg]
    record_class: Optional[Type]


class Settings(SettingsBaseModel):
    dsn: Optional[str] = None
    host: Optional[str] = None
    port: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    passfile: Optional[str] = None
    database: Optional[str] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    max_queries: Optional[int] = None
    max_inactive_connection_lifetime: Optional[float] = None
    setup: Optional[Any] = None
    init: Optional[Any] = None
    loop: Optional[Any] = None
    timeout: Optional[float] = None
    statement_cache_size: Optional[int] = None
    max_cached_statement_lifetime: Optional[float] = None
    max_cacheable_statement_size: Optional[int] = None
    command_timeout: Optional[float] = None
    ssl: Optional[str] = None
    direct_tls: Optional[bool] = None
    connection_class: Optional[Type[ConnectionAsyncpg]] = None
    record_class: Optional[Type] = None
    server_settings: Optional[dict] = None

    def database_settings(self):
        return getter_validate(DatabaseSettings)(getter_dict(self.__class__)(self))

    def connection_settings(self):
        return getter_validate(ConnectionSettings)(getter_dict(self.__class__)(self))

    def database_connect_kwargs(
        self, exclude_unset: bool = True, exclude_none: bool = True
    ):
        return self.database_settings().connect_kwargs(
            exclude_unset=exclude_unset, exclude_none=exclude_none
        )

    def connection_connect_kwargs(
        self, exclude_unset: bool = True, exclude_none: bool = True
    ):
        return self.connection_settings().connect_kwargs(
            exclude_unset=exclude_unset, exclude_none=exclude_none
        )
