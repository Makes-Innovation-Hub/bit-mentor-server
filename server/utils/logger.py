import logging
from logging.handlers import RotatingFileHandler
import os
import uuid


# Function to generate a unique request ID
def generate_request_id():
    return str(uuid.uuid4())


# Custom logging filter to add the request_id to the log records
class RequestIdFilter(logging.Filter):
    def __init__(self, request_id):
        super().__init__()
        self.request_id = request_id

    def filter(self, record):
        record.request_id = self.request_id
        return True


# Logger setup function
def setup_logger():
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Create a custom logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create handlers
    handler = RotatingFileHandler('logs/app.log', maxBytes=5000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(request_id)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


# Create a global logger instance
logger = setup_logger()
