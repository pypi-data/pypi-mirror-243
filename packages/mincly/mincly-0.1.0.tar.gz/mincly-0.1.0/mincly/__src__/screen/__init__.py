from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union
import mincly.__src__.utils as utils


T = TypeVar("T")


class Screen(ABC, Generic[T]):
    def __init__(self, screen_name: Union[str, None] = None) -> None:
        self.name = screen_name

    def __str__(self) -> str:
        return f"{self.__class__.__name__}('{self.name if self.name is not None else '<NoName>'}')"

    @abstractmethod
    def process_input(self, user_input: str) -> utils.Result[T]:
        raise NotImplementedError()

    @abstractmethod
    def get_display_string(self) -> str:
        raise NotImplementedError()
