import inspect
import time

from rich.console import Console

CURRENT_FUNCTION = 0
PREVIOUS_FUNCTION = 1


class SystemMessage:
    def __init__(self):
        pass

    @staticmethod
    def formatted_string(message, style):
        console = Console(color_system="truecolor")

        with console.capture() as capture:
            console.print("{style}{message}".format(
                message=message, style=style
            ))

        return capture.get().strip("\n")

    @staticmethod
    def print(message, style="[blue]"):
        function_name = inspect.stack()[PREVIOUS_FUNCTION].function
        print("[ {function_name} ]: {message}".format(
            function_name=SystemMessage.formatted_string(message=function_name, style=style), message=message
        ))