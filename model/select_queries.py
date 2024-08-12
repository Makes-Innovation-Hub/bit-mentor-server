from server.utils.logger import app_logger

def get_random_quotes(quotes_collection) -> list:
    """
    Retrieves a list of random quotes from the provided quotes collection.

    Args:
        quotes_collection: A MongoDB collection containing quotes.

    Returns:
        list: A list of random quotes, or an empty list if an error occurs.
    """
    try:
        quotes = list(quotes_collection.aggregate([{'$sample': {'size': 5}}]))
        return quotes
    except Exception as e:
        app_logger.error(f"Failed to get random quotes: {e}")
        return []
