# Yet Another Colorful Logger

## Description

Yet Another Colorful Logger is a just another Python logging utility that adds color to your console log messages. This module is already configured, not requiring setup. Simply install it and integrate into your Python projects.

This module was created for personal use, but feel free to use it in your projects as well. 
Also, feel free to customize it according to your needs.

Any issues, suggestions, or questions, please feel free to reach out.

## Installation

To install Yet Another Colorful Logger, use `pip`:

```bash
pip install yet-another-colorful-logger
```

## Usage

To start using the logger is pretty forward. Just import it and create a logger instance:

```python
from yaclogger import YACLogger

# Create a logger instance
logger = YACLogger(name="my_logger")

# Log messages with different severity levels
logger.debug("This is a debug message !!!")
logger.info("This is an info message !!!")
logger.warning("This is a warning message !!!")
logger.error("This is an error message !!!")
logger.critical("This is a critical message !!!")
```

![Yet Another Colorful Logger Example](/docs/images/example.png "Yet Another Colorful Logger Exame")

## Contact

For any questions, suggestions, or issues, feel free to reach out:

- GitHub: [Wagner Cotta](https://github.com/wagnercotta)

## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.