import typing as __t
from .common import Screen as __Screen
from ..utils import Err as __Err, Ok as __Ok, Result as __Result

__T = __t.TypeVar("__T")


class OptionScreen(__Screen[__T]):
    def __init__(
        self,
        numbered_options: __t.Tuple[__t.Tuple[str, __T]],
        keyword_options: __t.Dict[str, __t.Tuple[str, __T]],
        header: str = "Pick an option:",
        name: __t.Union[str, None] = None,
    ) -> None:
        super().__init__(name)
        self.numbered_options = numbered_options
        self.keyword_options = keyword_options
        self.header = header

    def process_input(self, user_input: str) -> __Result[__T]:
        if len(user_input) < 1:
            return __Err("Empty input")

        if user_input.isdecimal():
            nth_option = int(user_input) - 1
            if nth_option < 0 or nth_option >= len(self.numbered_options):
                return __Err(f"Invalid numbered option '{user_input}'")
            _, option = self.numbered_options[nth_option]
            return __Ok(option)

        _, option = self.keyword_options.get(user_input, ("", None))
        if option is None:
            return __Err(f"Invalid keyword option '{user_input}'")

        return __Ok(option)

    def get_display_string(self) -> str:
        display_string = f"{self.header}\n"

        for nth, (option_description, _) in enumerate(self.numbered_options, start=1):
            display_string += f" {nth} - {option_description}\n"

        if len(self.numbered_options) > 0:
            display_string += "\n"

        for key, (option_description, _) in self.keyword_options.items():
            display_string += f" {key} - {option_description}\n"

        if len(self.keyword_options) > 0:
            display_string += "\n"

        return display_string
