# LoggerUtility

`LoggerUtility` is a Python class that simplifies logging setup across your Python applications. It provides a streamlined way to configure loggers with custom formats, different logging levels, and optional file output. Whether you're debugging during development or monitoring in production, `LoggerUtility` can help you keep clear and concise logs.

## Features

- Easy logger configuration with just a few lines of code.
- Customizable log message format.
- Optional date formatting in log messages.
- Support for logging to console or files.
- Convenience methods for various logging levels (`debug`, `info`, `warning`, `error`, `critical`).

## Installation

You can simply copy the `LoggerUtility` class into your project, or if you have it packaged, you can install it via `pip` (assuming you have it available on PyPI):

```bash
pip install cd-logging
```
## Update

```bash
pip install -U cd-logging
```

## Usage

Here is a quick example of how to use `LoggerUtility`:

```python
from cd_logging.cd_logging import LoggerUtility

# Initialize the logger
logger_util = LoggerUtility(__name__, level=logging.INFO)

# Log some messages
logger_util.info("Application is starting...")
logger_util.warning("An optional warning message.")
logger_util.error("An error occurred.")

# Log a critical message with exception traceback
try:
    raise ValueError("An example exception.")
except Exception:
    logger_util.critical("A critical error occurred.", exc_info=True)
```

## Configuration

When initializing the `LoggerUtility`, you can customize the following:

- `name`: The logger's name, typically set to `__name__` to reflect the module's name.
- `level`: The threshold for the logging messages (e.g., `logging.DEBUG`, `logging.INFO`).
- `log_format`: Custom format for the log messages.
- `date_format`: Custom date format for the log messages.
- `filename`: If set, logs will be directed to the specified file.

## Documentation

For more details on how to use and configure `LoggerUtility`, please refer to the inline documentation within the class itself. Each method and initializer parameter is thoroughly documented with docstrings.

More documentation at:
[Code Docta](https://codedocta.com "Code Docta")

## Contributing

We welcome contributions from the community! If you'd like to contribute, feel free to fork the repository, make your changes, and submit a pull request.

## License

`LoggerUtility` is licensed under the MIT License. See the LICENSE file for more details.

## Contact

If you have any questions or feedback, please open an issue in the GitHub repository, and we will get back to you as soon as possible.
```

