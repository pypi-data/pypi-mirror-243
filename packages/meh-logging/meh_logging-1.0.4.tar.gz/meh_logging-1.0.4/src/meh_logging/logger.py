"""
    Logging module which implements MEH standards.
"""
import logging
import traceback

from .utils import package
from .enums.levels import Levels
from .transports.stream import StreamTransport

# Defaults
DEFAULT_MIN_LEVEL = Levels.NOT_SET.value
DEFAULT_MAX_LEVEL = Levels.MAX_LEVEL.value


class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, "_instance"):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class Logger(Singleton):
    def __init__(self, name=package.app_name):
        self.name = name

        logging.root.setLevel(DEFAULT_MIN_LEVEL)

        self.logger = logging.getLogger(name)
        self.add_transport(StreamTransport(level=Levels.DEBUG.value))

        if not name or name == package.FALLBACK_PACKAGE_NAME:
            self.warning(
                "No app name was found! A `package.json` file containing the app name is required in the root of the project (cwd)"
            )

    def __str__(self):
        return f"<Logger name={self.name}>"

    def set_level(self, level):
        self.logger.setLevel(level)

        for handler in self.logger.handlers:
            handler.setLevel(level)

        return self

    def __handle_stack(self, message):
        if isinstance(message, Exception):
            return {
                "stack": "".join(
                    traceback.TracebackException.from_exception(message).format()
                ),
            }

        return {"stack": None}

    def add_transport(self, handler):
        self.logger.addHandler(handler)
        return self

    def log(self, message, level):
        return self.logger.log(level.value, message, extra=self.__handle_stack(message))

    def debug(self, message):
        return self.log(message, Levels.DEBUG)

    def info(self, message):
        return self.log(message, Levels.INFO)

    def critical(self, message):
        return self.log(message, Levels.CRITICAL)

    def warning(self, message):
        return self.log(message, Levels.WARNING)

    def error(self, message):
        return self.log(message, Levels.ERROR)


logger = Logger()
