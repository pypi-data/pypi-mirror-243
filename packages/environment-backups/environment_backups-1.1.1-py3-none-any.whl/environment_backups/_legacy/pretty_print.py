from enum import Enum


class TerminalColor(str, Enum):
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END_COLOR = '\033[00m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_success(message):
    print_color(message, TerminalColor.OK_GREEN)


def print_warning(message):
    print_color(message, TerminalColor.WARNING)


def print_error(message):
    print_color(message, TerminalColor.ERROR)


def print_color(message: str, color: TerminalColor):
    print(f'{color.value}{message}{TerminalColor.END_COLOR}')
