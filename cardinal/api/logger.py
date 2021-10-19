"""Provides a decorator which logs all requests to a log file."""

from datetime import datetime
from os import path
from enum import Enum
from termcolor import colored

_FILE_PATH = "request_log.txt"

"""THE MAIN DECORATOR
Please look up how decorators work, but in essence:
@decorator
def function():
  # code
is equivalent to:
def function():
  # code
function = decorator(function)
This decorator is applied to every get operation so that each one has
logging code inserted.
"""


def request_logged(fn):
    def new_fn(cself, request, *args, **kwargs):
        logger(cself, request, fn, *args, **kwargs)
        return fn(cself, request, *args, **kwargs)

    return new_fn


# THE LOGGER
# Takes in the arguments and the function and spits out some logging info
def logger(cself, request, fn, *args, **kwargs):
    log_file = open(_FILE_PATH, "a")
    # So (classname).get
    name = fn.__qualname__
    # (classname).get -> ['classname', 'get'] -> 'classname'
    calling_class = name.split(".")[0]
    args_string = (
        "\n".join(("\t" + str(arg)) for arg in args) + "\n" if len(args) != 0 else "[no arguments]"
    )
    kwargs_string = (
        "\n".join(("\t" + f"{arg} : '{str(kwargs[arg])}'") for arg in kwargs.keys()) + "\n"
        if len(kwargs.keys()) != 0
        else "[no arguments]"
    )
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(
        f"""Date: {timestamp}
Request type: {calling_class}
Arguments: {args_string}
Keyword arguments: {kwargs_string}
Query params:
    {request.query_params}

"""
    )
    log_file.close()


class Severity(Enum):
    INFO = 0
    WARN = 1
    ERROR = 2
    DEBUG = 3
    FATAL = 4
    RAW = 5


def log(message: str, severity: Severity):
    # Print only the raw message
    if severity == Severity.RAW:
        print(message)
        return

    message_type = f"{severity.name}"

    if severity == Severity.WARN:
        message_type = colored(message_type, "yellow")
    elif severity == Severity.ERROR:
        message_type = colored(message_type, "red")
    elif severity == Severity.FATAL:
        message_type = colored(message_type, "red")
    elif severity == Severity.INFO:
        message_type = colored(message_type.lower(), "blue")

    message = f"{message_type}: {message}"
    print(message)

    # Quit the program if the severity is fatal
    if severity == Severity.FATAL:
        exit(-1)
