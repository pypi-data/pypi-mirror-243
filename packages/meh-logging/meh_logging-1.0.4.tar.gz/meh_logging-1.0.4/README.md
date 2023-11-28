### meh-logging-python

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

---

### Before you start

> To use the logging module in Python, you will need to have a Manifest file called `package.json` in the project's root folder. The file should follow the file structure guidelines provided at https://docs.npmjs.com/cli/v9/configuring-npm/package-json.

### Prerequisite software

The software listed below is required beforehand.

| Enum   | Value   |
| ------ | ------- |
| python | >= 3.10 |
| pip    | >= 22.2 |

### Installation

To install the module from your terminal, simply execute the following command:

```sh
$ pip install meh_logging
```

#### Usage

The logging module searches for an OS environment variable called `PYTHON_ENV` or `ENV`. If the variable is set to "production", the module will use the log level `INFO`; otherwise, it will use `DEBUG`.

```python
from meh_logging import logger, Levels

# Log some info
logger.info("hello world")
logger.debug("hello world")
logger.error("hello world")

# Log exception
try:
    1 / 0
except Exception as e:
    logger.info(e)

# Change log-level dynamically
logger.set_level(Levels().CRITICAL.value)
```

### Levels

These are the log levels utilized by the module.

| Enum           | Value |
| -------------- | ----- |
| NOT_SET        | 0     |
| DEBUG          | 10    |
| INFO           | 20    |
| WARNING / WARN | 30    |
| ERROR          | 40    |
| CRITICAL       | 50    |

#### Author(s)

[Jim de Ronde](https://github.com/jrtderonde)
