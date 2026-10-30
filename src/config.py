import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

SYMBOL = os.getenv("STOCK_SYMBOL", "IBM")

BASE_URL = "https://www.alphavantage.co/query"

API_URL = (
    f"{BASE_URL}"
    f"?function=TIME_SERIES_DAILY"
    f"&symbol={SYMBOL}"
    f"&apikey={API_KEY}"
)

CSV_OUTPUT_PATH = f"data/processed/{SYMBOL.lower()}_stock_data.csv"