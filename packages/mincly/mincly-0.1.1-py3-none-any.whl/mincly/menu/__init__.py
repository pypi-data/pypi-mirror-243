import mincly.__src__.io as io
import mincly.__src__.io.standard as stdio


class Menu:
    def __init__(
        self,
        input_output: io.Io = None,
        input: io.In = None,
        output: io.Out = None,
    ) -> None:
        self.__io: io.Io
        if input_output is not None:
            self.__io = input_output
        elif input is not None or output is not None:
            input_or_standard = (
                input if input is not None else stdio.StandardTerminalIn()
            )
            output_or_standard = (
                output if output is not None else stdio.StandardTerminalOut()
            )
            self.__io = io.HybridIo(input_or_standard, output_or_standard)
        else:
            self.__io = stdio.StandardTerminalIo()
