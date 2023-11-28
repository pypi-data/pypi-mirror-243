"""
Generate the app defaults
"""
import platform
import os
import re

from datetime import datetime
from .read_package import read_package_file

# Platform consts
PLATFORM = "python"
PLATFORM_VERSION = platform.python_version()

# Fallbacks
FALLBACK_PACKAGE_NAME = "unknown-app"
FALLBACK_PACKAGE_VERSION = "0.0.0"

PYTHON_ENV = os.getenv("ENV", os.getenv("PYTHON_ENV", ""))


def parse_app_name(name):
    if PYTHON_ENV == "acceptance":
        return re.sub("-acc$", "", name)
    elif PYTHON_ENV == "test":
        return re.sub("-test$", "", name)

    return name


package = read_package_file()

app_name = package.get("name", FALLBACK_PACKAGE_NAME)
app_name = parse_app_name(app_name)
app_version = package.get("version", FALLBACK_PACKAGE_VERSION)

JSON_DEFAULTS = {
    "appName": app_name,
    "appVersion": app_version,
    "platform": PLATFORM,
    "platformVersion": PLATFORM_VERSION,
    "timestamp": datetime.now().astimezone().isoformat(),
}
