import os as __os
from . import In as __In, Out as __Out


class AnsiTerminalOut(__Out):
    """For ANSI compliant terminals, everything outputed to this terminal is
    stored and can be cleared and overwritten at any type. For it to work
    properly, this must be the only source of printed content."""

    def __init__(
        self,
        add_newline_to_prints: bool = False,
        always_flush: bool = True,
    ) -> None:
        self.__last_printed_content: str = ""
        self.__print_options = {}
        self.__print_options["end"] = "\n" if add_newline_to_prints else ""
        if always_flush:
            self.__print_options["flush"] = True

    def output(self, value: str):
        """Prints message to terminal. Avoid using ANSI control sequence
        characters in `value`"""
        self.__last_printed_content += value + self.__print_options["end"]
        print(value, **self.__print_options)

    def print_overwrite(self, value: str):
        """Clears printed contents and prints `value`"""
        self.clear()
        self.print(value)

    def clear_last_n_lines(self, n: int):
        """Clears last `n` lines in terminal. Does not change internal printed
        content, you may use this method to rectify content printed outside this
        class."""
        if n < 1:
            return
        clear_string = "\033[2K"
        if n > 1:
            clear_string += "\033[A\033[2K" * (n - 1)
        print(clear_string, end="", flush=True)

    def clear(self):
        """Clears all content that this class printed. Does not account for
        printed content from other sources"""
        if self.__last_printed_content is None:
            return
        terminal_width = __os.get_terminal_size().columns
        printed_lines = self.__last_printed_content.split("\n")
        number_of_lines_in_terminal = 0
        for printed_line in printed_lines:
            number_of_lines_in_terminal += 1
            remaining_string = printed_line
            while len(remaining_string) > terminal_width:
                number_of_lines_in_terminal += 1
                remaining_string = remaining_string[terminal_width:]
        self.clear_last_n_lines(number_of_lines_in_terminal)
        self.__last_printed_content = ""


class AnsiTerminalIo(AnsiTerminalOut, __In):
    """For ANSI compliant terminals, everything outputed to this terminal is
    stored and can be cleared and overwritten at any type. For it to work
    properly, this must be the only source of printed content.

    `get_input()` method is counted towards printed content for the purposes of
    `clear`ing the terminal."""

    def get_input(self) -> str:
        """Retrieves input using Python's builtin `input` method. Takes into
        account the user's input and newline character (ENTER) for the next call
        to `clear()`."""
        user_input = input()
        self.__last_printed_content += user_input + "\n"
        return user_input
