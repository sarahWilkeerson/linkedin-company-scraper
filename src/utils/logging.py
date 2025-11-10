import logging as _pylog
import os
import sys

def _level():
    return os.getenv("LOG_LEVEL", "INFO").upper()

def get_logger(name: str) -> _pylog.Logger:
    logger = _pylog.getLogger(name)
    if logger.handlers:
        return logger
    handler = _pylog.StreamHandler(stream=sys.stdout)
    fmt = _pylog.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.setLevel(_level())
    # quiet noisy libraries
    _pylog.getLogger("aiohttp.access").setLevel("WARNING")
    _pylog.getLogger("aiohttp.client").setLevel("WARNING")
    return logger