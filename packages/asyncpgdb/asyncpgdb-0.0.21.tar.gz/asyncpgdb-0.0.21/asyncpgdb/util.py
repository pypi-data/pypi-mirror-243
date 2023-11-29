from typing import Callable, Type, TypeVar

T = TypeVar("T")

def getter(__model,__attrs):
    return next(
        (
            getattr(__model,attr)
            for attr in __attrs if hasattr(__model,attr)
        ),
        None
    )

def getter_validate(__model:Type[T],attrs=("model_validate", "parse_obj")) -> Callable[...,T]:
    return getter(__model,attrs)

def getter_dict(__model:Type[T],attrs=("model_dump", "dict")) -> Callable[...,dict]:
    return getter(__model,attrs)

def parse_obj( __model: Type[T],__obj) -> T:
    return getter_validate(__model)(__obj)

def parse_dict(__model: Type[T],__obj) -> dict:
    return getter_dict(__model)(__obj)


