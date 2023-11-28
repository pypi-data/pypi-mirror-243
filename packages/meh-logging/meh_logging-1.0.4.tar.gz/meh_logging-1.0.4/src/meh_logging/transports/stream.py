import sys
from logging import StreamHandler

from ..formatters.json import JSONFormatter


class StreamTransport(StreamHandler):
    def __init__(self, **kwargs):
        level = kwargs.get("level")
        StreamHandler.__init__(self)

        self.setLevel(level)
        self.setFormatter(JSONFormatter())

    def emit(self, record):
        message = self.format(record)
        return sys.stdout.write(message + "\n")
