import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Comma-separated list, e.g. STOCK_SYMBOLS=IBM,AAPL,MSFT
SYMBOLS = [
    s.strip().upper()
    for s in os.getenv("STOCK_SYMBOLS", "IBM").split(",")
    if s.strip()
]

# "compact" = last ~100 trading days, "full" = 20+ years of history
OUTPUT_SIZE = os.getenv("OUTPUT_SIZE", "compact")

BASE_URL = "https://www.alphavantage.co/query"

# Free tier allows 5 requests/minute
API_DELAY_SECONDS = int(os.getenv("API_DELAY_SECONDS", "13"))

CHART_OUTPUT_DIR = "visualization/output"
