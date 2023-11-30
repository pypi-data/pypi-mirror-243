# wai-logging
Simple helper library for logging.

## Methods

* `init_logging` - initializes the logging with a default level, which can be overridden with an environment variable
* `set_logging_level` - sets the logging level of a `logging.Logger` instance
* `str_to_logging_level` - turns a string logging level into a `logging` module one, used by `init_logging` and `set_logging_level`
* `add_logging_level` - adds an option for the logging level to an `argparse.ArgumentParser` instance
* `add_logger_name` - adds an option for a custom name for a logger to an `argparse.ArgumentParser` instance
