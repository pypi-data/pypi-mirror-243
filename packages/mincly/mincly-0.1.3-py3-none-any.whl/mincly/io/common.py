import abc as __abc


class In(__abc.ABC):
    @__abc.abstractmethod
    def get_input(self) -> str:
        """Collect input from user or any source."""
        raise NotImplementedError()


class Out(__abc.ABC):
    @__abc.abstractmethod
    def output(self, message: str):
        """Sends message to output (e.g. by printing)."""
        raise NotImplementedError()

    @__abc.abstractmethod
    def clear(self):
        """Clears output (e.g. by removing printed content)"""
        raise NotImplementedError()


class Io(In, Out):
    pass


class HybridIo(Io):
    def __init__(self, input: In, output: Out) -> None:
        self.__in = input
        self.__out = output

    def output(self, message: str):
        return self.__out.output(message)

    def clear(self):
        return self.__out.clear()

    def get_input(self) -> str:
        return self.__in.get_input()
