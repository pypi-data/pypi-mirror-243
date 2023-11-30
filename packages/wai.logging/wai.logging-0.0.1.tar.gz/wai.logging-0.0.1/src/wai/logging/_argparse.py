import argparse

from ._core import LOGGING_LEVELS, LOGGING_WARN


def add_logging_level(parser: argparse.ArgumentParser, short_opt: str = "-l", long_opt: str = "--logging_level",
                      help_str: str = None):
    """
    Adds an option for the logging level to the parser.

    :param parser: the parser to append.
    :type parser: argparse.ArgumentParser
    :param short_opt: the short option flag to use (eg -l)
    :type short_opt: str
    :param long_opt: the long option flag to use (eg --logging_level)
    :type long_opt: str
    :param help_str: the help string to use
    :type help_str: str
    """
    if help_str is None:
        help_str = "The logging level to use."
    parser.add_argument(short_opt, long_opt, choices=LOGGING_LEVELS, default=LOGGING_WARN, help=help_str)


def add_logger_name(parser: argparse.ArgumentParser, short_opt: str = "-N", long_opt: str = "--logger_name",
                    help_str: str = None):
    """
    Adds an option for the logger name to the parser.

    :param parser: the parser to append.
    :type parser: argparse.ArgumentParser
    :param short_opt: the short option flag to use (eg -N)
    :type short_opt: str
    :param long_opt: the long option flag to use (eg --logger_name)
    :type long_opt: str
    :param help_str: the help string to use
    :type help_str: str
    """
    if help_str is None:
        help_str = "The custom name to use for the logger"
    parser.add_argument(short_opt, long_opt, type=str, default=None, help=help_str, required=False)
