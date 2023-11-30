import inspect
import time

from colorama import Fore, Back, Style

CURRENT_FUNCTION = 0
PREVIOUS_FUNCTION = 1


class SystemMessage:
    def __init__(self):
        pass

    @staticmethod
    def error(message, **kwargs):
        function_name = inspect.stack()[PREVIOUS_FUNCTION].function
        print("[ {time} ] [{level}] [{function}]: {message}".format(
            function=function_name,
            message=message,
            level=SystemMessage.red("error"),
            time=time.strftime("%x %H:%M:%S %Z", time.localtime()),
            **kwargs
        ))

    @staticmethod
    def info(message, **kwargs):
        function_name = inspect.stack()[PREVIOUS_FUNCTION].function
        print("[ {time} ] [{level}] [{function}]: {message}".format(
            function=function_name,
            message=message,
            level=SystemMessage.blue("info"),
            time=time.strftime("%x %H:%M:%S %Z", time.localtime()),
            **kwargs
        ))

    @staticmethod
    def debug(message, **kwargs):
        function_name = inspect.stack()[PREVIOUS_FUNCTION].function
        print("[ {time} ] [{level}] [{function}]: {message}".format(
            function=function_name,
            message=message,
            level=SystemMessage.green("debug"),
            time=time.strftime("%x %H:%M:%S %Z", time.localtime()),
            **kwargs
        ))

    @staticmethod
    def warning(message, **kwargs):
        function_name = inspect.stack()[PREVIOUS_FUNCTION].function
        print("[ {time} ] [{level}] [{function}]: {message}".format(
            function=function_name,
            message=message,
            level=SystemMessage.yellow("warning"),
            time=time.strftime("%x %H:%M:%S %Z", time.localtime()),
            **kwargs
        ))

    @staticmethod
    def critical(message, **kwargs):
        function_name = inspect.stack()[PREVIOUS_FUNCTION].function
        print("[ {time} ] [{level}] [{function}]: {message}".format(
            function=function_name,
            message=message,
            level=SystemMessage.red_highlight("CRITICAL"),
            time=time.strftime("%x %H:%M:%S %Z", time.localtime()),
            **kwargs
        ))

    @staticmethod
    def red(message):
        return Style.BRIGHT + Fore.RED + message + Style.RESET_ALL

    @staticmethod
    def red_highlight(message):
        return Style.BRIGHT + Back.RED + Fore.WHITE + message + Style.RESET_ALL

    @staticmethod
    def blue(message):
        return Style.BRIGHT + Fore.BLUE + message + Style.RESET_ALL

    @staticmethod
    def blue_dim(message):
        return Style.DIM + Fore.BLUE + message + Style.RESET_ALL

    @staticmethod
    def green(message):
        return Style.BRIGHT + Fore.GREEN + message + Style.RESET_ALL

    @staticmethod
    def magenta(message):
        return Style.BRIGHT + Fore.MAGENTA + message + Style.RESET_ALL

    @staticmethod
    def magenta_dim(message):
        return Style.DIM + Fore.MAGENTA + message + Style.RESET_ALL

    @staticmethod
    def cyan(message):
        return Style.DIM + Fore.CYAN + message + Style.RESET_ALL

    @staticmethod
    def yellow(message):
        return Style.BRIGHT + Fore.YELLOW + message + Style.RESET_ALL

    @staticmethod
    def grey(message):
        return Style.DIM + Fore.WHITE + message + Style.RESET_ALL
