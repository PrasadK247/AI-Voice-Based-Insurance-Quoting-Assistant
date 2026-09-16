"""
UC189 - Logger utility
"""

import sys
import logging
from typing import Optional

try:
    from loguru import logger as loguru_logger
    _USE_LOGURU = True
except ImportError:
    _USE_LOGURU = False


def setup_logger(name: Optional[str] = None):
    """Set up and return a structured logger instance."""
    if _USE_LOGURU:
        # Avoid duplicate handlers
        return loguru_logger.bind(name=name or "UC189")
    else:
        logger = logging.getLogger(name or "UC189")
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
