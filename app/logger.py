import os
import logging
from logging.handlers import TimedRotatingFileHandler

from app.config import config

os.makedirs(config.APP_LOG_PATH, exist_ok=True)

logger = logging.getLogger("APP_LOGGER")
logger.setLevel(logging.INFO)


if not logger.handlers:
    log_format = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(config.APP_LOG_PATH, "app.log"),
        when="midnight",
        interval=1,
        backupCount=config.APP_LOG_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
