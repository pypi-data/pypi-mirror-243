import re as __re
import typing as __t
from .common import Screen as __Screen
from ..utils import Err as __Err, Ok as __Ok, Result as __Result


class ConfirmScreen(__Screen[bool]):
    def __init__(
        self,
        message: str,
        true_regex: str = r"^[Yy]|[Yy][Ee][Ss]$",
        default_no_input: __t.Union[bool, None] = None,
        screen_name: __t.Union[str, None] = None,
    ) -> None:
        super().__init__(screen_name)
        self.message = message
        self.true_regex = __re.compile(true_regex)
        self.default = default_no_input

    def get_display_string(self) -> str:
        return self.message

    def process_input(self, user_input: str) -> __Result[bool]:
        if self.true_regex.match(user_input):
            return __Ok(True)
        elif len(user_input) < 1:
            return (
                __Err("Empty input")
                if self.default is None
                else __Ok(self.default)
            )
        else:
            return __Ok(False)
