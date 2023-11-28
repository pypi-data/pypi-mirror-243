import abc as __abc
import typing as __t
from ..utils import Result as __Result


__T = __t.TypeVar("__T")


class Screen(__abc.ABC, __t.Generic[__T]):
    def __init__(self, screen_name: __t.Union[str, None] = None) -> None:
        self.name = screen_name

    def __str__(self) -> str:
        return f"{self.__class__.__name__}('{self.name if self.name is not None else '<NoName>'}')"

    @__abc.abstractmethod
    def process_input(self, user_input: str) -> __Result[T]:
        raise NotImplementedError()

    @__abc.abstractmethod
    def get_display_string(self) -> str:
        raise NotImplementedError()
