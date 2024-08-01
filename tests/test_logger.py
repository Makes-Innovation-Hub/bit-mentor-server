import logging
import os
from server.utils.logger import setup_logger, RequestIdFilter, generate_request_id

# Define the base directory and log directory according to your setup
base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
log_directory = os.path.join(base_directory, 'logs')

print(f"Test - Base directory: {base_directory}")  # Debug message
print(f"Test - Log directory: {log_directory}")  # Debug message

def test_log_file_creation():
    request_id = generate_request_id()
    logger = setup_logger()
    request_filter = RequestIdFilter(request_id)
    logger.addFilter(request_filter)
    assert os.path.exists(log_directory), f"Log directory does not exist: {log_directory}"
    assert os.path.exists(os.path.join(log_directory, 'app.log')), "Log file does not exist."
    logger.removeFilter(request_filter)

def test_log_file_rotation():
    request_id = generate_request_id()
    logger = setup_logger()
    request_filter = RequestIdFilter(request_id)
    logger.addFilter(request_filter)

    for i in range(2000):
        logger.info(f"Log message {i}")

    log_files = [f for f in os.listdir(log_directory) if f.startswith('app.log')]
    assert len(log_files) > 1, "Log rotation did not occur."

    logger.removeFilter(request_filter)

def test_log_message():
    request_id = generate_request_id()
    logger = setup_logger()
    request_filter = RequestIdFilter(request_id)
    logger.addFilter(request_filter)

    test_message = "This is a test log message"
    logger.info(test_message)

    log_file_path = os.path.join(log_directory, 'app.log')
    assert os.path.exists(log_file_path), f"Log file does not exist: {log_file_path}"
    with open(log_file_path, 'r') as log_file:
        log_content = log_file.read()
        assert request_id in log_content, "Request ID not found in log output."
        assert test_message in log_content, "Test message not found in log output."

    logger.removeFilter(request_filter)

def test_logger_creation():
    request_id = generate_request_id()
    logger = setup_logger()
    request_filter = RequestIdFilter(request_id)
    logger.addFilter(request_filter)

    assert isinstance(logger, logging.Logger)
    logger.info("Logger creation test passed.")

    logger.removeFilter(request_filter)

if __name__ == "__main__":
    test_log_file_creation()
    test_log_file_rotation()
    test_log_message()
    test_logger_creation()
    print("All tests passed.")
