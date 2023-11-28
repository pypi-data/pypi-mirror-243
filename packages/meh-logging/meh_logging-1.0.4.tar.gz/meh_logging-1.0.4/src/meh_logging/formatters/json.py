import json

from logging import Formatter
from ..utils.package import JSON_DEFAULTS


class JSONFormatter(Formatter):
    def __init__(self):
        super().__init__()

    def __format(self, record):
        message = record.message
        level = record.levelname
        obj = {"level": level.lower(), "message": str(message)} | JSON_DEFAULTS

        if hasattr(record, "stack") and record.stack is not None:
            obj["stack"] = record.stack

        return json.dumps(obj)

    def formatMessage(self, record):
        return self.__format(record)
