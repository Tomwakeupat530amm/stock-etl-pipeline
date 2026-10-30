import requests

from src.config import API_URL
from src.logger import logger


def extract_stock_data():
    """
    Fetch stock market data from Alpha Vantage API.

    Returns:
        dict: Complete JSON response as Python dictionary.
    """

    try:

        logger.info("Calling Alpha Vantage API")

        response = requests.get(API_URL, timeout=30)

        response.raise_for_status()

        data = response.json()

        logger.info("API Response Received")

        if "Time Series (Daily)" not in data:

            logger.error(f"Unexpected API Response: {data}")

            raise ValueError(
                f"Unexpected API Response: {data}"
            )

        return data

    except Exception as e:

        logger.exception(f"Extraction Failed: {e}")

        raise