from server.utils.logger import app_logger

def get_random_quotes(quotes_collection) -> list:
    try:
        quotes = list(quotes_collection.aggregate([{'$sample': {'size': 5}}]))
        return quotes
    except Exception as e:
        app_logger.error(f"Failed to get random quotes: {e}")
        return []
