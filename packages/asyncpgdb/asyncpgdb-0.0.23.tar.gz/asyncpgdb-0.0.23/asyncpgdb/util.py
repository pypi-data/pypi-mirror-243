from typing import Callable, Type, TypeVar
from pydantic import __version__ as _pydantic_version


if _pydantic_version.startswith("1"):
    _model_parser_attr = "parse_obj"
    _model_dict_attr = "dict"
elif _pydantic_version.startswith("2"):
    _model_parser_attr = "model_validate"
    _model_dict_attr = "model_dump"
else:
    raise ImportError("Unable to import pydantic v1* or v2*")

T = TypeVar("T")


def getter_validate(__model: Type[T]) -> Callable[..., T]:
    return getattr(__model, _model_parser_attr)


def getter_dict(__model: Type[T]) -> Callable[..., dict]:
    return getattr(__model, _model_dict_attr)
