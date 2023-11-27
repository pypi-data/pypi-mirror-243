import logging


class LoggerUtility:
    """
    A utility class for configuring and using logging.
    """

    def __init__(self, name, level=logging.DEBUG, log_format=None, date_format=None, filename=None):
        """
        Initializes the LoggerUtility.

        :param name: Name for the logger. Typically, you'd use __name__.
        :type name: str
        :param level: Logging level. Defaults to logging.DEBUG.
        :type level: int
        :param log_format: Format for the logging messages.
                           Defaults to '%(asctime)s - %(levelname)s - %(message)s'.
        :type log_format: str
        :param date_format: Format for the date in the logging messages.
                            Defaults to '%Y/%m/%d %I:%M:%S %p'.
        :type date_format: str
        :param filename: If specified, logs will be written to this file instead of console.
        :type filename: str
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if log_format is None:
            log_format = '%(asctime)s - %(levelname)s - %(message)s'

        if date_format is None:
            date_format = '%Y/%m/%d %I:%M:%S %p'

        formatter = logging.Formatter(log_format, datefmt=date_format)

        if filename:
            handler = logging.FileHandler(filename)
        else:
            handler = logging.StreamHandler()

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log(self, msg, level=logging.INFO):
        """
        Logs a message with the specified level.

        :param msg: The message to log.
        :type msg: str
        :param level: Logging level. Defaults to logging.INFO.
        :type level: int
        """
        self.logger.log(level, msg)

    def debug(self, msg):
        """
        Logs a debug message.

        :param msg: The message to log.
        :type msg: str
        """
        self.logger.debug(msg)

    def info(self, msg):
        """
        Logs an info message.

        :param msg: The message to log.
        :type msg: str
        """
        self.logger.info(msg)

    def warning(self, msg):
        """
        Logs a warning message.

        :param msg: The message to log.
        :type msg: str
        """
        self.logger.warning(msg)

    def error(self, msg):
        """
        Logs an error message.

        :param msg: The message to log.
        :type msg: str
        """
        self.logger.error(msg)

    def critical(self, msg):
        """
        Logs a critical message.

        :param msg: The message to log.
        :type msg: str
        """
        self.logger.critical(msg)

