# LoggerPlus

A wrapper around Python's built-in logging module.

## Goals

- Provide a drop-in replacement for Python's logging module.
- Provide highly verbose exception tracebacks with variable context. You will see the values of the variables at each and every level in the traceback.
- Provide extensive defaults for logging configuration so you don't have to worry about it.
- Provide colored logs in cross-platform-agnostic manner
- Almost zero overhead on the main thread.
- Fix some annoying issues with Python's logging module.
- Handle scenarios when the user forgets to initialize the logger, or uses it incorrectly. Using RobustLogger in any way shape or form should never throw an exception outside of the RobustLogger library itself (they will be logged to a file).

## Installation

You can install the package via pip:

```bash
pip install LoggerPlus
```

## Usage

To use the package, you can import it and use it as a drop-in replacement for Python's logging module.

```python
from loggerplus import RobustLogger

if __name__ == "__main__":
    logger = RobustLogger()
    logger.debug("This is a debug message")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
    RobustLogger.debug("This is a debug message, correctly handling a user forgetting to construct RobustLogger.")  # type: ignore[call-arg, arg-type]

    # Test various edge case
    RobustLogger("This is a test of __call__")  # type: ignore[call-arg]

    try:
        raise RuntimeError("Test caught exception")  # noqa: TRY301
    except RuntimeError:
        RobustLogger().exception("Message for a caught exception")
    raise RuntimeError("Test uncaught exception")
```

The example code demonstrates how to use the `RobustLogger` class from the `LoggerPlus` package. It shows the following:

1. **Initialization**: A `RobustLogger` instance is created.
2. **Logging Messages**: Various log levels are used to log messages (`debug`, `info`, `warning`, `error`, `critical`).
3. **Handling Edge Cases**: The `RobustLogger` class is used directly to handle a case where the user forgets to construct the logger.
4. **Exception Logging**: The code demonstrates how to log caught and uncaught exceptions using the `exception` method of `RobustLogger`.

This example highlights the ease of use and robustness of the `RobustLogger` class.

## How does it work?

LoggerPlus achieves its goals through the following mechanisms:

1. **Drop-in Replacement**: The `RobustRootLogger` class is designed to be a drop-in replacement for Python's built-in logging module. It inherits from `logging.Logger` and uses a metaclass `MetaLogger` to ensure a singleton instance, making it easy to use without additional setup.

2. **Extensive Defaults**: The `_setup_logger` method in `RobustRootLogger` configures multiple handlers and formatters by default. It sets up handlers for console output, file logging for different log levels, and exception logging. This ensures that users get a comprehensive logging setup out of the box.

3. **Colored Logs**: The `ColoredConsoleHandler` class extends `logging.StreamHandler` and uses the `colorama` library to provide colored log output. This makes logs easier to read and distinguish based on log levels.

4. **Minimal Main Thread Logic**: The `_log` method in `RobustRootLogger` ensures that logging is done in a separate thread using `ThreadPoolExecutor`. This prevents logging operations from blocking the main thread, improving performance and responsiveness.

5. **Robustness**: The `RobustRootLogger` class and its associated methods handle various edge cases, such as when the user forgets to initialize the logger or uses it incorrectly. The `CustomPrintToLogger` class redirects `stdout` and `stderr` to the logger, ensuring that all output is captured. Additionally, the `CustomExceptionFormatter` and `format_exception_with_variables` functions provide detailed exception information, making it easier to debug issues.

6. **Dynamic Attribute Access**: The `__getattribute__` method in `RobustRootLogger` ensures that any attribute access is handled dynamically, allowing for robust error handling and logging. This method, combined with the metaclass `MetaLogger`, ensures that the logger instance is always available and properly configured.

## Why not just use loguru?

Loguru is a more modern library, and it has a lot of features that Python's logging module does not have.  Truthfully, I had not heard of Loguru, until AFTER I finished this library.

Loguru is a great library, and I recommend it if you want a more powerful and flexible logging solution. However, it is not a drop-in replacement for Python's logging module, and it requires a different way of logging to work.

Basically, if you want to use a different logging library, you have to change your code. LoggerPlus allows you to use the same API you're used to, but with more features.

## Enhanced Traceback Functionality

A common problem I personally have is getting a traceback and not understanding context. What variables/attributes/arguments contents were? Unless I was in a debug environment, I'd have no idea. Users would send me tracebacks all the time, yet I'd have no idea what was happening at the point of the error.

LoggerPlus also provides enhanced traceback functionality. When an exception is raised, LoggerPlus captures and logs detailed information about the exception, including the stack trace and local variables at each frame. This makes it easier to debug issues by providing more context about the error.

For example, when a `RuntimeError` is raised, LoggerPlus logs the following information:

```powershell
ERROR(root): Message for a caught exception

----------------------------------------------------------------
Traceback (most recent call last):
  File "C:\GitHub\LoggerPlus\loggerplus\__init__.py", line 682, in <module>
    raise RuntimeError("Test caught exception")  # noqa: TRY301
RuntimeError: Test caught exception

RuntimeError: Test caught exception
Stack Trace Variables:

Function '<module>' at C:\GitHub\LoggerPlus\loggerplus\__init__.py:682:
  __annotations__ = {}
  annotations = _Feature((3, 7, 0, 'beta', 1), (3, 10, 0, 'alpha', 0), 16777216)
  logging = <module 'logging' from 'C:\\Program Files\\Python38\\lib\\logging\\__init__.py'>
  multiprocessing = <module 'multiprocessing' from 'C:\\Program Files\\Python38\\lib\\multiprocessing\\__init__.py'>
  os = <module 'os' from 'C:\\Program Files\\Python38\\lib\\os.py'>
  shutil = <module 'shutil' from 'C:\\Program Files\\Python38\\lib\\shutil.py'>
  sys = <module 'sys' (built-in)>
  threading = <module 'threading' from 'C:\\Program Files\\Python38\\lib\\threading.py'>
  time = <module 'time' (built-in)>
  uuid = <module 'uuid' from 'C:\\Program Files\\Python38\\lib\\uuid.py'>
  ThreadPoolExecutor = <class 'concurrent.futures.thread.ThreadPoolExecutor'>
  contextmanager = <function contextmanager at 0x000001E0FF352AF0>
  suppress = <class 'contextlib.suppress'>
  RotatingFileHandler = <class 'logging.handlers.RotatingFileHandler'>
  Path = <class 'pathlib.Path'>
  TYPE_CHECKING = False
  Any = typing.Any
  ClassVar = typing.ClassVar
  format_exception_with_variables = _lru_cache_wrapper(
    )
  UTF8StreamWrapper = <class '__main__.UTF8StreamWrapper'>
  LOGGING_LOCK = <unlocked _thread.lock object at 0x000001E0FF915660>
  THREAD_LOCAL = _local(
    is_logging=True
)
  logging_context = <function logging_context at 0x000001E0FFF34AF0>
  get_this_child_pid = <function get_this_child_pid at 0x000001E0FFF34B80>
  CustomPrintToLogger = <class '__main__.CustomPrintToLogger'>
  SafeEncodingLogger = <class '__main__.SafeEncodingLogger'>
  CustomExceptionFormatter = <class '__main__.CustomExceptionFormatter'>
  ColoredConsoleHandler = <class '__main__.ColoredConsoleHandler'>
  LogLevelFilter = <class '__main__.LogLevelFilter'>
  _dir_requires_admin = <function _dir_requires_admin at 0x000001E0FFF34C10>
  _delete_any_file_or_folder = <function _delete_any_file_or_folder at 0x000001E0FFF36700>
  get_log_directory = <function get_log_directory at 0x000001E0FFF36790>
  _get_fallback_log_dir = <function _get_fallback_log_dir at 0x000001E0FFF36820>
  _safe_isfile = <function _safe_isfile at 0x000001E0FFF368B0>
  _safe_isdir = <function _safe_isdir at 0x000001E0FFF36940>
  _SpoofTypeAttributeAccess = <class '__main__._SpoofTypeAttributeAccess'>
  _SpoofObjectAttributeAccess = <class '__main__._SpoofObjectAttributeAccess'>
  MetaLogger = <class '__main__.MetaLogger'>
  _safe_print = <function _safe_print at 0x000001E0FFF369D0>
  RobustLogger = <class '__main__.RobustLogger'>
  get_root_logger = <class '__main__.RobustLogger'>
  logger = <RootLogger root (DEBUG)>
Traceback (most recent call last):
  File "C:\GitHub\LoggerPlus\loggerplus\__init__.py", line 682, in <module>
    raise RuntimeError("Test caught exception")  # noqa: TRY301
RuntimeError: Test caught exception

----------------------------------------------------------------
```

This enhanced traceback functionality provides a comprehensive view of the error, making it easier to identify and fix issues in your code.

Overall, LoggerPlus provides a powerful and user-friendly logging solution that meets the goals

## License

This project is licensed under the LGPLv2.1 License. See the LICENSE file for more details.
