from typing import List, Union, Any, TypeVar
import mincly.__src__.menu as menu
import mincly.__src__.io as io
import mincly.__src__.screen as screen
import mincly.__src__.utils as utils

T = TypeVar("T")


class NavigableMenu(menu.Menu):
    def __init__(
        self,
        input_output: io.Io = None,
        input: io.In = None,
        output: io.Out = None,
        input_message: str = "Your input: ",
    ) -> None:
        super().__init__(input_output, input, output)
        self.__screen_stack: List[screen.Screen] = []
        self.__input_preamble = input_message

    def show(self, message: str):
        """Shows a message without expecting any input from the user"""
        self.__io.print_overwrite(message)

    def push(self, screen: screen.Screen[T]) -> T:
        """Displays the provided screen, which is added to this NavigableMenu
        instance's stack.

        Screen will only be displayed when calling `get_input()`"""
        self.__screen_stack.append(screen)

    def pop(self):
        """Pops current screen from the stack and returns to last found screen.
        If the current screen is the only screen in the stack, this method will
        raise an exception."""

        if len(self.__screen_stack) < 2:
            raise RuntimeError(
                "Can't navigate back when current screen is root screen."
            )
        self.__screen_stack.pop()

    def get_input(self) -> Any:
        """Blocks until user provides a valid input. 'Valid input' is defined by
        the `Screen` class that is on the top of the screen stack."""
        self.prompt(self.__screen_stack[-1])

    def prompt(self, screen: screen.Screen[T]) -> T:
        """Displays the provided screen. Blocks until user provides a valid
        input.

        Provided screen is not added to screen stack and will not be stored
        by this `NavigableMenu` instance."""
        screen_result: Union[utils.Result, None] = None

        while screen_result is None or screen_result.is_err():
            self.__io.print_overwrite(screen.get_display_string())

            if screen_result is not None and screen_result.is_err():
                self.__io.print(f"<ERROR>: {screen_result.unwrap_err()}\n")

            self.__io.print(self.__input_preamble)
            user_input = self.__io.input()

            screen_result = screen.process_input(user_input)

        return screen_result.unwrap()

    def current_screen_name(self) -> Union[str, None]:
        return self.__screen_stack[-1].name
