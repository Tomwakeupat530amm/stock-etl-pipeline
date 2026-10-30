from pathlib import Path

from sqlalchemy import text

from src.database import engine
from src.logger import logger

DDL_PATH = Path(__file__).resolve().parent.parent / "sql" / "create_tables.sql"

UPSERT = text("""
    INSERT INTO daily_stock_prices
        (symbol, trade_date, open_price, high_price, low_price,
         close_price, volume, daily_return)
    VALUES
        (:symbol, :trade_date, :open_price, :high_price, :low_price,
         :close_price, :volume, :daily_return)
    ON CONFLICT (symbol, trade_date) DO UPDATE SET
        open_price   = EXCLUDED.open_price,
        high_price   = EXCLUDED.high_price,
        low_price    = EXCLUDED.low_price,
        close_price  = EXCLUDED.close_price,
        volume       = EXCLUDED.volume,
        daily_return = EXCLUDED.daily_return
""")


def ensure_table():
    """Create the target table if it does not exist yet."""
    with engine.begin() as conn:
        conn.exec_driver_sql(DDL_PATH.read_text())


def load_to_postgres(df) -> int:
    """Upsert the DataFrame (bulk). Returns number of rows sent."""

    records = [
        {
            "symbol": r.symbol,
            "trade_date": r.date.date(),
            "open_price": float(r.open_price),
            "high_price": float(r.high_price),
            "low_price": float(r.low_price),
            "close_price": float(r.close_price),
            "volume": int(r.volume),
            # NaN (first row) -> NULL
            "daily_return": None if r.daily_return != r.daily_return else float(r.daily_return),
        }
        for r in df.itertuples(index=False)
    ]

    with engine.begin() as conn:
        conn.execute(UPSERT, records)

    logger.info(f"Upserted {len(records)} rows for {df['symbol'].iloc[0]}")
    return len(records)
