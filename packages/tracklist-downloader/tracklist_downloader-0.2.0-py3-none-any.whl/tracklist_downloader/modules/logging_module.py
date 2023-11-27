import logging


class CustomFormatter(logging.Formatter):
    """
    Custom formatter to differentiate error messages from other log levels.
    """

    # Override format method
    def format(self, record):
        # Original format
        original_format = '%(asctime)s [%(levelname)s] %(name)s (%(module)s:%(funcName)s:%(lineno)d): %(message)s'

        # Custom format for ERROR and higher levels
        if record.levelno >= logging.ERROR:
            self._style._fmt = '%(asctime)s [%(levelname)s] [ERROR] %(name)s (%(module)s:%(funcName)s:%(lineno)d): %(message)s %(exc_info)s'
        else:
            self._style._fmt = original_format

        return super(CustomFormatter, self).format(record)


def setup_logger(debug: bool =False) -> logging.Logger:
    """
        Sets up and configures a logger for the application.

        Args:
        - debug (bool): If True, sets the logger level to DEBUG. Defaults to False.

        Returns:
        - logging.Logger: Configured logger instance.
    """
    # Create a logger
    logger = logging.getLogger('spotLy')
    logger.setLevel(logging.DEBUG if debug else logging.WARNING)

    # Create handlers
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('spotLy.log', mode="w")
    file_handler.setLevel(logging.DEBUG)

    # Create formatter and add it to handlers
    formatter = CustomFormatter()
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


class FileErrorHandler(logging.Handler):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def emit(self, record):
        if record.levelno >= logging.ERROR:
            with open(self.filepath, 'a') as file:
                file.write(self.format(record) + '\n')
