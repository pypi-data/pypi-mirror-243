"""
"""
import os
from .logger import logger
from .transports import StreamTransport
from .enums.levels import Levels

env_value = os.getenv("PYTHON_ENV", os.getenv("ENV", "production"))

if env_value == "production":
    logger.set_level(Levels.INFO.value)
else:
    logger.set_level(Levels.DEBUG.value)
