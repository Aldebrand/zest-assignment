####################################################
# This file encapsulates the logger configuration. #
# A rotating file handler is employed for logging  #
# in this project, serving as a pragmatic choice   #
# given the time constraints. While alternative    #
# logging handlers, like those sending logs to     #
# databases such as Elasticsearch or message       #
# queues like Kafka, could have been utilized to   #
# enhance log management and analysis, the         #
# integration of such technologies was deferred    #
# due to the limited time available. This          #
# approach enables a balance between functionality #
# and development efficiency, ensuring adequate    #
# logging capabilities for the current scope of    #
# the project.                                     #
####################################################


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
file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
file_handler.setLevel(logging.INFO)

# Create stream handler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)

# Create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
