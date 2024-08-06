import pytest
import logging
import re
import os
import asyncio
from fastapi.testclient import TestClient

from server.utils.logger import setup_logger, generate_request_id, RequestIdFilter
from server.server import app as fastapi_app

# Define the base directory and log directory according to your setup
base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
log_directory = os.path.join(base_directory, 'logs')
log_file_path = os.path.join(log_directory, 'app.log')


@pytest.fixture(scope="module", autouse=True)
def setup_logging():
    setup_logger()


@pytest.fixture
def app():
    return fastapi_app


def test_singleton_behavior():
    logger1 = setup_logger()
    logger2 = setup_logger()
    assert logger1 is logger2


def test_log_file_creation():
    setup_logger()
    assert os.path.exists(log_directory), f"Log directory does not exist: {log_directory}"
    assert os.path.exists(log_file_path), "Log file does not exist."


def test_single_log_file():
    setup_logger()
    log_files = [f for f in os.listdir(log_directory) if f.startswith('app.log')]
    assert len(log_files) == 1, f"Expected 1 log file, but found {len(log_files)}."


def extract_request_ids_from_log():
    request_ids = set()
    log_pattern = re.compile(r' - ([0-9a-fA-F-]+) - ')
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            match = log_pattern.search(line)
            if match:
                request_id = match.group(1)
                request_ids.add(request_id)
    return request_ids


def flush_logs():
    for handler in logging.getLogger('app_logger').handlers:
        handler.flush()


def test_unique_request_id_per_api_request(app):
    client = TestClient(app)

    client.get("/")
    client.get("/")

    flush_logs()

    request_ids = extract_request_ids_from_log()
    assert len(request_ids) >= 2, "Not enough request IDs found in log."
    assert len(request_ids) == len(set(request_ids)), "Request IDs are not unique."


def test_request_id_consistency(app):
    client = TestClient(app)

    client.get("/")

    flush_logs()

    request_ids = extract_request_ids_from_log()
    assert len(request_ids) >= 1, "Request ID not found in log."
    request_id = list(request_ids)[0]

    with open(log_file_path, 'r') as log_file:
        log_content = log_file.read()
        assert log_content.count(request_id) > 1, "Request ID is not consistent throughout the log."


@pytest.mark.asyncio
async def test_singleton_logger_handling_async_requests(app):
    client = TestClient(app)

    async def make_request():
        return client.get("/")

    tasks = [make_request() for _ in range(5)]
    await asyncio.gather(*tasks)

    flush_logs()

    request_ids = extract_request_ids_from_log()
    assert len(request_ids) >= 5, "Not enough request IDs found in log."
    assert len(set(request_ids)) == len(request_ids), "Request IDs are not unique in concurrent requests."
    for request_id in request_ids:
        with open(log_file_path, 'r') as log_file:
            log_content = log_file.read()
            assert log_content.count(request_id) > 1, f"Request ID {request_id} is not consistent throughout the log."


if __name__ == '__main__':
    pytest.main()
