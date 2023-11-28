import typing as __t

__T = __t.TypeVar("__T")
__R = __t.TypeVar("__R")


class Result(__t.Generic[__T]):
    """Util class to wrap around fallible values instead of raising Exceptions.
    Do not instantiate direcly, instead, use `Err` and `Ok` util functions from
    this package"""

    def __init__(self, value: __t.Union[__T, Exception], is_ok: bool):
        self.__value = value
        self.__is_ok = is_ok

    @staticmethod
    def from_func(
        func: __t.Callable[[None], __R], catch_system_errors: bool = False
    ) -> "Result[__R]":
        catch_target = BaseException if catch_system_errors else Exception
        try:
            return Ok(func())
        except catch_target as e:
            return Err(e)

    def is_ok(self) -> bool:
        """Returns `True` if this `Result` is of the `Ok` type"""
        return self.__is_ok

    def is_err(self) -> bool:
        """Returns `True` if this `Result` is of the `Err` type"""
        return not self.__is_ok

    def unwrap(self) -> __T:
        """Returns the wrapped value if this `Result` is `Ok`, else, if this
        `Result` is `Err`, then raises the wrapped exception, instead."""
        if self.__is_ok:
            return self.__value
        else:
            raise self.__value

    def try_unwrap(self) -> __t.Union[__T, None]:
        """Returns the wrapped value if this `Result` is `Ok`, else, if this
        `Result` is `Err`, returns `None`."""
        if self.__is_ok:
            return self.__value
        else:
            return None

    def unwrap_err(self) -> BaseException:
        """Returns the wrapped exception if this `Result` is `Err`, else, if
        this `Result` is `Ok`, then raises a `TypeError`."""
        if not self.__is_ok:
            return self.__value
        else:
            raise TypeError("Can't unwrap error type in instance of Ok result.")


def Err(error: __t.Union[BaseException, str]) -> Result[__T]:
    """Instantiate Error Result which wraps around exception. If `error` is
    a string, will instantiate an `Exception` with `error` as error message."""
    if isinstance(error, str):
        return Result(Exception(error), False)
    return Result(error, False)


def Ok(value: __T) -> Result[__T]:
    """Instantiate Ok Result which wraps around a `value` (use `None` if
    value is irrelevant)"""
    return Result(value, True)
