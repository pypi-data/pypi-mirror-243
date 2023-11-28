import logging
from enum import Enum


class Levels(Enum):
    NOT_SET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    WARN = WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    MAX_LEVEL = logging.CRITICAL + 10
