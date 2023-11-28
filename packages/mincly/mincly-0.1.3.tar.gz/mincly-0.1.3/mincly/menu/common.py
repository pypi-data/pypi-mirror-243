from ..io import (
    Io as __Io,
    Out as __Out,
    In as __In,
    HybridIo as __HybridIo,
    StandardTerminalIn as __StandardTerminalIn,
    StandardTerminalOut as __StandardTerminalOut,
    StandardTerminalIo as __StandardTerminalIo,
)


class Menu:
    def __init__(
        self,
        input_output: __Io = None,
        input: __In = None,
        output: __Out = None,
    ) -> None:
        self.__io: __Io
        if input_output is not None:
            self.__io = input_output
        elif input is not None or output is not None:
            input_or_standard = input if input is not None else __StandardTerminalIn()
            output_or_standard = (
                output if output is not None else __StandardTerminalOut()
            )
            self.__io = __HybridIo(input_or_standard, output_or_standard)
        else:
            self.__io = __StandardTerminalIo()
