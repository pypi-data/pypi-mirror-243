"""
"""
import os
import json

# Package.json consts
PACKAGE_FILE_NAME = "package.json"
PACKAGE_LOCATION = os.path.join(os.getcwd(), PACKAGE_FILE_NAME)
ENCODING = "utf-8"


def read_package_file():
    try:
        file = open(PACKAGE_LOCATION, encoding=ENCODING)
        return json.load(file)
    except Exception:
        return {}
