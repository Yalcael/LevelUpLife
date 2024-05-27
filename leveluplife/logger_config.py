from sys import stderr

from loguru import logger


def filter_record(record):
    if "lul" in record["file"].path:
        return True
    return False


def configure_logger():
    logger.configure(
        handlers=[{"sink": stderr, "filter": filter_record, "backtrace": False}]
    )
