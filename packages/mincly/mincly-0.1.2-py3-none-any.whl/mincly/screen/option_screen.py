from typing import Dict, Tuple, TypeVar, Union
import mincly.__src__.screen as screen
import mincly.__src__.utils as utils

T = TypeVar("T")


class OptionScreen(screen.Screen[T]):
    def __init__(
        self,
        numbered_options: Tuple[Tuple[str, T]],
        keyword_options: Dict[str, Tuple[str, T]],
        header: str = "Pick an option:",
        name: Union[str, None] = None,
    ) -> None:
        super().__init__(name)
        self.numbered_options = numbered_options
        self.keyword_options = keyword_options
        self.header = header

    def process_input(self, user_input: str) -> utils.Result[T]:
        if len(user_input) < 1:
            return utils.Err("Empty input")

        if user_input.isdecimal():
            nth_option = int(user_input) - 1
            if nth_option < 0 or nth_option >= len(self.numbered_options):
                return utils.Err(f"Invalid numbered option '{user_input}'")
            _, option = self.numbered_options[nth_option]
            return utils.Ok(option)

        _, option = self.keyword_options.get(user_input, ("", None))
        if option is None:
            return utils.Err(f"Invalid keyword option '{user_input}'")

        return utils.Ok(option)

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
