"""pyaslengine.log"""

import logging


def get_logger(name, propagate=True):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = propagate
    return logger


def set_logging_level(level):
    logging.getLogger("pyaslengine").setLevel(level)
