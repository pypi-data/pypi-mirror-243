import re
from typing import Union
import mincly.__src__.screen as screen
import mincly.__src__.utils as utils


class ConfirmScreen(screen.Screen[bool]):
    def __init__(
        self,
        message: str,
        true_regex: str = r"^[Yy]|[Yy][Ee][Ss]$",
        default_no_input: Union[bool, None] = None,
        screen_name: Union[str, None] = None,
    ) -> None:
        super().__init__(screen_name)
        self.message = message
        self.true_regex = re.compile(true_regex)
        self.default = default_no_input

    def get_display_string(self) -> str:
        return self.message

    def process_input(self, user_input: str) -> utils.Result[bool]:
        if self.true_regex.match(user_input):
            return utils.Ok(True)
        elif len(user_input) < 1:
            return (
                utils.Err("Empty input")
                if self.default is None
                else utils.Ok(self.default)
            )
        else:
            return utils.Ok(False)
