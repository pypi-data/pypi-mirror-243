from typing import Callable, Optional


def handle_exception(
    __exc_id: str, __exc: Exception, log: Optional[Callable[..., None]] = None
):
    exception = f"{str(type(__exc).__name__)}: {str(__exc)}"
    message = f"{__exc_id}: {exception}"
    (print if log is None else log)(message)
