import sys
import logging

class Logger():
    """
    @version 1.2.0

    Logger class implementing the singleton pattern, to keep a single instance across all the operations.
    It implements the logging module, which supports log levels, handlers (for stream and file outputs), 
    as well as formatting.
    The Logger should be initialized once in the application entry point or root. Before calling the initialize
    method, we can change the log_level, log_format and output_file_name. Once initialized, the format and 
    output file cannot be changed.
    """
    #Logger instance
    instance: logging.Logger = None

    # Log level
    log_level = logging.WARNING

    # Logging format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'

    # Output log file name
    output_log_file_name = 'session.log'

    @staticmethod
    def initialize(
        level = logging.WARNING,
        verbose = False
    ):
        """
        @param {int} level The logger minimum level to display.
        @param {bool} verbose A flag that indicates if the INFO messages should be displayed as minimum level.
        
        Sets the basic config for the logger, specifying the log level, as well as the format and handlers
        (for stream and file outputs). Finally, we set the Singleton instance.
        """
        # If the instance was already set, we skip this process
        if Logger.instance: return
        # We get the logger handlers (stream and file)
        logger_handlers = Logger.__get_handlers()

        # We change the level to INFO if the verbose flag was enabled
        level = level if not verbose else logging.INFO
       
        # We set the logger basic config, setting the log level, format and handletrs
        logging.basicConfig(
            level = level,
            format = Logger.log_format,
            handlers = logger_handlers
        )

        # Finally, we set the loger instance
        Logger.instance = logging.getLogger()

    @staticmethod
    def set_level(level: int):
        """
        @param {int} level Logger level to set.

        Sets the logger level at run time.
        """
        if not Logger.instance:
            raise Exception('Logger not initialized')
        Logger.instance.setLevel(level)

    @staticmethod
    def get_instance():
        """
        Singleton method to get the logger instance. It allows safe operation if the Logger is
        not initialized manually by the user.
        """
        if not Logger.instance:
            Logger.initialize()
        return Logger.instance

    @staticmethod
    def info(message: str):
        """
        @param {str} message The message to log.

        Logs a message at INFO level.
        """
        Logger.get_instance().info(message)

    @staticmethod
    def debug(message: str, *args, **kwargs):
        """
        @param {str} message The message to log.
        
        Logs a message at DEBUG level.
        """
        Logger.get_instance().debug(message, *args, **kwargs)
    
    @staticmethod
    def error(message: str, *args, **kwargs):
        """
        @param {str} message The message to log.
        
        Logs a message at ERROR level.
        """
        Logger.get_instance().error(message, *args, **kwargs)

    @staticmethod
    def warning(message: str, *args, **kwargs):
        """
        @param {str} message The message to log.
        
        Logs a message at WARNING level.
        """
        Logger.get_instance().warning(message, *args, **kwargs)

    @staticmethod
    def critical(message: str, *args, **kwargs):
        """
        @param {str} message The message to log.
        
        Logs a message at CRITICAL level.
        """
        Logger.get_instance().critical(message, *args, **kwargs)

    @staticmethod
    def exception(message: str, *args, **kwargs):
        """
        @param {str} message The message to log.
        
        Logs an exception (including the stack trace).
        """
        Logger.get_instance().exception(message, *args, **kwargs)

    # Utils
    @staticmethod
    def get_normalized_logger_level(level: int) -> int:
        """
        @param {int} level The number that represents the logger level.

        Normalizes a given level, if it is in scale of 1, it scales it by 10 to fit.
        Intended for use with CLI count arguments, which give us a number from 1 to 5.

        @returns Normalized level.
        """
        if level == 0:
            return level
        elif level > 0 and level < 10:
            return level * 10
        else: return level

    # Private methods
    @staticmethod
    def __get_handlers() -> list:
        """
        Initializes the handlers and return them as a list.

        @returns List of handlers.
        """
        file_handler = logging.FileHandler(filename = Logger.output_log_file_name)
        stdout_handler = logging.StreamHandler(sys.stdout)
        return [file_handler, stdout_handler]



        