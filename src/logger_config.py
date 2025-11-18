import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # make sure logs/ exists

def get_logger(name: str, filename: str):
    log_file = os.path.join(LOG_DIR, filename)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # avoid duplicate logs if called multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
