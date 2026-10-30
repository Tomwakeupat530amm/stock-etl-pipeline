from sqlalchemy import text
from src.database import engine


def load_to_postgres(df):
    """
    Load DataFrame into PostgreSQL.
    """

    insert_query = text("""
        INSERT INTO daily_stock_prices
        (
            trade_date,
            open_price,
            high_price,
            low_price,
            close_price,
            volume
        )

        VALUES
        (
            :trade_date,
            :open_price,
            :high_price,
            :low_price,
            :close_price,
            :volume
        )

        ON CONFLICT (trade_date)
        DO NOTHING;
    """)
    with engine.begin() as conn:

        for _, row in df.iterrows():

            conn.execute(

                insert_query,

                {
                    "trade_date": row["date"].date(),

                    "open_price": float(row["open_price"]),

                    "high_price": float(row["high_price"]),

                    "low_price": float(row["low_price"]),

                    "close_price": float(row["close_price"]),

                    "volume": int(row["volume"])
                }

            )

    print("Data Loaded Successfully.")  