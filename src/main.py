import argparse
import sys
import time

from src.config import API_DELAY_SECONDS, SYMBOLS
from src.extract import extract_stock_data
from src.load import ensure_table, load_to_postgres
from src.logger import logger
from src.transform import transform_stock_data
from visualization.charts import generate_all_charts


def run_symbol(symbol: str) -> None:
    raw = extract_stock_data(symbol)
    df = transform_stock_data(raw, symbol)
    logger.info(f"[{symbol}] Transformed {len(df)} rows")
    load_to_postgres(df)
    generate_all_charts(df, symbol)


def main(symbols=None) -> None:
    symbols = symbols or SYMBOLS
    logger.info(f"ETL started for: {', '.join(symbols)}")

    ensure_table()

    failed = []
    for i, symbol in enumerate(symbols):
        if i:
            time.sleep(API_DELAY_SECONDS)  # respect API rate limit
        try:
            run_symbol(symbol)
            logger.info(f"[{symbol}] OK")
        except Exception as e:
            logger.exception(f"[{symbol}] FAILED: {e}")
            failed.append(symbol)

    if failed:
        raise RuntimeError(f"ETL failed for: {', '.join(failed)}")
    logger.info("ETL finished successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock ETL pipeline")
    parser.add_argument("--symbol", "-s", nargs="+", help="override STOCK_SYMBOLS")
    args = parser.parse_args()
    try:
        main([s.upper() for s in args.symbol] if args.symbol else None)
    except Exception:
        sys.exit(1)
