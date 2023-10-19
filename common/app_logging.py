import logging
from logging.handlers import RotatingFileHandler
import sys

MAX_BYTES = 1024 * 1024
BACKUP_COUNT = 5
LOG_FILE_PATH = './logs/service.log'

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create file handler
file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
file_handler.setLevel(logging.INFO)

# Create stream handler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
