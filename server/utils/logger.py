import logging
from logging.handlers import RotatingFileHandler
import os
import uuid


def generate_request_id():
    return str(uuid.uuid4())


class RequestIdFilter(logging.Filter):
    def __init__(self, request_id):
        super().__init__()
        self.request_id = request_id if request_id is not None else 'no-request-id'

    def filter(self, record):
        record.request_id = self.request_id
        return True


_logger_initialized = False


def setup_logger():
    global _logger_initialized
    logger_name = 'app_logger'
    logger = logging.getLogger(logger_name)

    if _logger_initialized:
        return logger

    logger.setLevel(logging.INFO)
    base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    log_directory = os.path.join(base_directory, 'logs')
    if not os.path.exists(log_directory):
        print(f"Creating log directory: {log_directory}")
        os.makedirs(log_directory)

    log_file = os.path.join(log_directory, 'app.log')
    handler = RotatingFileHandler(log_file, maxBytes=5000, backupCount=0)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(request_id)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    print(f"Logger setup complete. Logs will be saved to: {log_file}")
    _logger_initialized = True
    return logger


app_logger = setup_logger()
