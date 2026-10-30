import pandas as pd

COLUMN_MAP = {
    "1. open": "open_price",
    "2. high": "high_price",
    "3. low": "low_price",
    "4. close": "close_price",
    "5. volume": "volume",
}


def transform_stock_data(data: dict, symbol: str) -> pd.DataFrame:
    """Turn the raw API response into a clean DataFrame.

    Columns: date, symbol, open_price, high_price, low_price, close_price,
    volume, daily_return (% change of close), ma20 (20-day moving average).
    """

    df = pd.DataFrame(data["Time Series (Daily)"]).T.rename(columns=COLUMN_MAP)
    df = df[list(COLUMN_MAP.values())].apply(pd.to_numeric, errors="coerce")

    df.index = pd.to_datetime(df.index)
    df.index.name = "date"
    df = df.sort_index()

    # Drop duplicate dates (not duplicate values) and invalid rows
    df = df[~df.index.duplicated(keep="last")].dropna()

    # Basic sanity checks on prices
    df = df[(df[["open_price", "high_price", "low_price", "close_price"]] > 0).all(axis=1)]
    df = df[df["high_price"] >= df["low_price"]]

    df["daily_return"] = df["close_price"].pct_change().mul(100).round(4)
    df["ma20"] = df["close_price"].rolling(window=20).mean().round(2)

    df.insert(0, "symbol", symbol)
    return df.reset_index()
