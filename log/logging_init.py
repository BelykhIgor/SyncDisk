import logging
import os
from logging.handlers import RotatingFileHandler

current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
log_file = os.path.join(current_directory, 'log.log')

logger = logging.getLogger("Synchronization")
logger.setLevel(logging.INFO)

if logger.hasHandlers():
    logger.handlers.clear()

file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding='utf-8')

# stream_handler = log.StreamHandler()
# file_handler = log.FileHandler("log.log", mode="a", encoding="UTF-8")
formatter = logging.Formatter(
    fmt="%(filename)s | %(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
# stream_handler.setFormatter(formatter)
# log.addHandler(stream_handler)
logger.propagate = False



