import requests

from src.config import API_KEY, BASE_URL, OUTPUT_SIZE
from src.logger import logger


def extract_stock_data(symbol: str) -> dict:
    """Fetch daily time series for one symbol from Alpha Vantage."""

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": OUTPUT_SIZE,
        "apikey": API_KEY,
    }

    try:
        logger.info(f"[{symbol}] Calling Alpha Vantage API")

        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        if "Time Series (Daily)" not in data:
            raise ValueError(f"Unexpected API response for {symbol}: {data}")

        return data

    except Exception as e:
        logger.exception(f"[{symbol}] Extraction failed: {e}")
        raise
