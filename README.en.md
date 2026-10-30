# stock-etl-pipeline

[Tiếng Việt](README.md) | **English**

An end-to-end stock-market ETL pipeline. It pulls daily prices for one or more tickers from the Alpha Vantage API, cleans and enriches them with Pandas, upserts them into PostgreSQL, generates charts, and is scheduled by Apache Airflow running in Docker.

## Features

- **Multi-symbol**: configure any number of tickers (`STOCK_SYMBOLS=IBM,AAPL,MSFT`).
- **Enriched data**: daily return (%) and 20-day moving average are computed in the transform step.
- **Validation**: invalid numbers, non-positive prices, `high < low` and duplicate dates are removed.
- **Idempotent upsert**: bulk `INSERT ... ON CONFLICT (symbol, trade_date) DO UPDATE`, so reruns never duplicate rows and corrected data overwrites old values.
- **Self-provisioning**: the target table is created automatically on first run.
- **One Airflow task per symbol**, run sequentially to respect the API rate limit; one failing symbol does not stop the others.
- **Charts per symbol** saved in `visualization/output/<SYMBOL>/`: closing price, volume, moving average, daily-return histogram, box plot, correlation heatmap.

## Architecture

```text
Alpha Vantage API -> extract.py -> transform.py -> load.py (PostgreSQL)
                                        |
                                        +-> visualization/charts.py (PNG)

Airflow DAG (daily 22:00 Asia/Ho_Chi_Minh): etl_ibm >> etl_aapl >> ...
   each task runs: python -m src.main --symbol <SYMBOL>
```

## Project structure

```text
stock-etl-pipeline/
├── airflow/dags/financial_etl_dag.py   # DAG: one task per symbol
├── src/
│   ├── config.py      # env-based settings
│   ├── database.py    # SQLAlchemy engine
│   ├── extract.py     # Alpha Vantage client
│   ├── transform.py   # cleaning, validation, return & MA20
│   ├── load.py        # table creation + bulk upsert
│   ├── logger.py
│   └── main.py        # CLI entry point
├── visualization/charts.py
├── sql/create_tables.sql
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
└── .env.example
```

## Configuration

Copy `.env.example` to `.env`:

```env
ALPHA_VANTAGE_API_KEY=your_api_key
STOCK_SYMBOLS=IBM,AAPL,MSFT
OUTPUT_SIZE=compact          # compact = ~100 days, full = 20+ years

DB_HOST=host.docker.internal
DB_PORT=5432
DB_NAME=stock_market
DB_USER=postgres
DB_PASSWORD=your_password

AIRFLOW_UID=50000
FERNET_KEY=                  # python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

The free Alpha Vantage tier is limited (about 5 requests/minute and a small daily quota), so keep the symbol list short. `API_DELAY_SECONDS` (default 13) controls the pause between symbols.

## Usage

### With Airflow (Docker)

```bash
docker compose up airflow-init
docker compose up -d
```

Open http://localhost:8080 (default login `airflow` / `airflow`), enable `financial_etl_pipeline` and trigger it, or wait for the 22:00 schedule. Create the `stock_market` database in PostgreSQL beforehand; the table is created automatically.

Stop with `docker compose down`.

### Without Airflow

```bash
pip install -r requirements.txt
python -m src.main                      # uses STOCK_SYMBOLS
python -m src.main --symbol NVDA TSLA   # override symbols
```

### Query the data

```sql
SELECT symbol, trade_date, close_price, daily_return
FROM daily_stock_prices
WHERE symbol = 'IBM'
ORDER BY trade_date DESC
LIMIT 10;
```

## Notes

- Educational project; market data may be delayed and is not investment advice.
- Airflow's generated `airflow.cfg` files contain secrets and are git-ignored.
- Default Airflow credentials and JWT secret in `docker-compose.yaml` are for local development only.
