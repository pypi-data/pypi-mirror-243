from typing import Generic, TypeVar, Union, Callable

T = TypeVar("T")
R = TypeVar("R")


class Result(Generic[T]):
    """Util class to wrap around fallible values instead of raising Exceptions.
    Do not instantiate direcly, instead, use `Err` and `Ok` util functions from
    this package"""

    def __init__(self, value: Union[T, Exception], is_ok: bool):
        self.__value = value
        self.__is_ok = is_ok

    @staticmethod
    def from_func(
        func: Callable[[None], R], catch_system_errors: bool = False
    ) -> "Result[R]":
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

    def unwrap(self) -> T:
        """Returns the wrapped value if this `Result` is `Ok`, else, if this
        `Result` is `Err`, then raises the wrapped exception, instead."""
        if self.__is_ok:
            return self.__value
        else:
            raise self.__value

    def try_unwrap(self) -> Union[T, None]:
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


def Err(error: Union[BaseException, str]) -> Result[T]:
    """Instantiate Error Result which wraps around exception. If `error` is
    a string, will instantiate an `Exception` with `error` as error message."""
    if isinstance(error, str):
        return Result(Exception(error), False)
    return Result(error, False)


def Ok(value: T) -> Result[T]:
    """Instantiate Ok Result which wraps around a `value` (use `None` if
    value is irrelevant)"""
    return Result(value, True)
