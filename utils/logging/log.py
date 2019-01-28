import logging
import logging.handlers

import traceback


class Log:
    """DarkLight Logger."""
    __logger = logging.getLogger('dlLogger')
    __logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s|%(asctime)s] %(message)s')

    # Stream log handler
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    __logger.addHandler(streamHandler)

    # File log handler
    """
    fileHandler = logging.FileHandler('engine.log')
    fileHandler.setFormatter(formatter)

    __logger.addHandler(fileHandler)
    """

    @classmethod
    def d(cls, message):
        # debug log
        cls.__logger.debug(message)

    @classmethod
    def i(cls, message):
        # info log
        cls.__logger.info(message)

    @classmethod
    def w(cls, message):
        # warning log
        cls.__logger.warning(message)

    @classmethod
    def e(cls, message, trace_exc=True):
        # error log
        if trace_exc:
            error = traceback.format_exc()
            cls.__logger.error(f"{message}\n{error}")
        else:
            cls.__logger.error(f"{message}")

    @classmethod
    def c(cls, message):
        # critical log
        cls.__logger.critical(message)
