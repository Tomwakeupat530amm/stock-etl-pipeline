import pandas as pd


def transform_stock_data(data: dict) -> pd.DataFrame:
    """
    Transform raw API response into a clean Pandas DataFrame.

    Args:
        data (dict): JSON response from Alpha Vantage.

    Returns:
        pd.DataFrame: Clean stock DataFrame.
    """

    # Extract Time Series
    time_series = data["Time Series (Daily)"]

    # Dictionary → DataFrame
    df = pd.DataFrame(time_series).T

    # Rename Columns
    df.columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    # Convert Data Types
    numeric_columns = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Convert Index to Datetime
    df.index = pd.to_datetime(df.index)

    # Name the Index
    df = df.rename(columns={
    "Open": "open_price",
    "High": "high_price",
    "Low": "low_price",
    "Close": "close_price",
    "Volume": "volume"
    })

    df.index.name = "trade_date"

    # Sort by Date
    df = df.sort_index()

    # Remove Duplicate Dates
    df = df.drop_duplicates()

    # Remove rows containing invalid values
    df = df.dropna()
    df = df.reset_index()
    df.rename(columns={"trade_date": "date"}, inplace=True)
    return df