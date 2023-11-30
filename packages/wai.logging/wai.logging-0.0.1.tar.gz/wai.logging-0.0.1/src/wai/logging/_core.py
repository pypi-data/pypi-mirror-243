import logging
import os


LOGGING_DEBUG = "DEBUG"
LOGGING_INFO = "INFO"
LOGGING_WARN = "WARN"
LOGGING_WARNING = "WARNING"
LOGGING_ERROR = "ERROR"
LOGGING_CRITICAL = "CRITICAL"
LOGGING_LEVELS = [
    LOGGING_DEBUG,
    LOGGING_INFO,
    LOGGING_WARNING,
    LOGGING_ERROR,
    LOGGING_CRITICAL,
]


def str_to_logging_level(level: str) -> int:
    """
    Turns a logging level string into the corresponding integer constant.

    :param level: the level to convert
    :type level: str
    :return: the int level
    :rtype: int
    """
    level = level.upper()
    if level == LOGGING_WARN:
        level = LOGGING_WARNING
    if level not in LOGGING_LEVELS:
        raise Exception("Invalid logging level (%s): %s" % ("|".join(LOGGING_LEVELS), level))
    if level == LOGGING_CRITICAL:
        return logging.CRITICAL
    elif level == LOGGING_ERROR:
        return logging.ERROR
    elif level == LOGGING_WARNING:
        return logging.WARNING
    elif level == LOGGING_INFO:
        return logging.INFO
    elif level == LOGGING_DEBUG:
        return logging.DEBUG
    else:
        raise Exception("Unhandled logging level: %s" % level)


def init_logging(default_level: str = LOGGING_WARNING, env_var: str = None):
    """
    Initializes the logging.

    :param default_level: the default level to use
    :type default_level: str
    :param env_var: the environment variable to check for a level (overrides the default level), ignored if None
    :type env_var: str
    """
    level = str_to_logging_level(default_level)
    if env_var is not None:
        if os.getenv(env_var) is not None:
            level = str_to_logging_level(os.getenv(env_var))
    logging.basicConfig(level=level)


def set_logging_level(logger: logging.Logger, level: str):
    """
    Sets the logging level of the logger.

    :param logger: the logger to update
    :type logger: logging.Logger
    :param level: the level string, see LOGGING_LEVELS
    :type level: str
    """
    logger.setLevel(str_to_logging_level(level))
