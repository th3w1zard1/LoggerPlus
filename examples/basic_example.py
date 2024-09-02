from __future__ import annotations

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
