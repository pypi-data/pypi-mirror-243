import mincly.__src__.io as io


class StandardTerminalOut(io.Out):
    """Basic output to terminal. `output()` is Python's builtin `print()` and
    `clear()` prints empty lines to create separation"""

    def __init__(
        self,
        add_newline_to_prints: bool = False,
        always_flush: bool = True,
        newlines_added_on_clear: int = 5,
    ) -> None:
        self.__print_options = {}
        self.__print_options["end"] = "\n" if add_newline_to_prints else ""
        if always_flush:
            self.__print_options["flush"] = True
        self.__clear_lines = max(0, newlines_added_on_clear)

    def output(self, value: str):
        """Prints message to terminal. Avoid using ANSI control sequence
        characters in `value`"""
        print(value, **self.__print_options)

    def print_overwrite(self, value: str):
        """Clears printed contents and prints `value`"""
        self.clear()
        self.print(value)

    def clear(self):
        """Prints newlines to screen to create separation from previous prints."""
        print("\n" * self.__clear_lines, end="")


class StandardTerminalIn(io.In):
    """Basic input from terminal. `get_input()` is Python's builtin `input()`."""

    def get_input(self) -> str:
        """Retrieves input using Python's builtin `input` method. Takes into
        account the user's input and newline character (ENTER) for the next call
        to `clear()`."""
        return input()


class StandardTerminalIo(io.HybridIo):
    """Hybrid of `StandardTerminalIn` and `StandardTerminalOut`."""
    def __init__(self) -> None:
        super().__init__(StandardTerminalIn(), StandardTerminalOut())