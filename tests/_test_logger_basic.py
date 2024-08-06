import logging

from server.utils.logger import setup_logger, RequestIdFilter, generate_request_id


def main():
    logger = setup_logger()
    request_id = generate_request_id()
    logger.addFilter(RequestIdFilter(request_id))

    try:
        logger.info("Starting the application")
        logger.debug("This is a debug message.")

        perform_operation_that_logs_info(logger)
        logger.warning("This is a warning message.")
        simulate_error(logger)
        raise Exception("Critical issue occurred!")
    except Exception as e:
        logger.critical(f"A critical error has occurred: {str(e)}", exc_info=True)


def perform_operation_that_logs_info(logger):
    logger.info("Performing a regular operation.")


def simulate_error(logger):
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error("An error occurred: Division by zero", exc_info=True)


if __name__ == "__main__":
    main()