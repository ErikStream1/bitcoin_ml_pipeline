from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator
import logging
import time

@contextmanager
def log_step(logger: logging.Logger, step: str)->Iterator[None]:
    start = time.perf_counter()
    logger.info("Running %s", step)
    
    try:
        yield
    except Exception:
        logger.exception("FAILED %s", step)
        raise
    
    else:
        elapsed = time.perf_counter() - start
        logger.info("Done %s (%.2fs)", step, elapsed)
        