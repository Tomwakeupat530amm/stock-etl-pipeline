# stock-etl-pipeline

An end-to-end financial data engineering pipeline that extracts daily stock market data from the Alpha Vantage API, transforms and validates the data using Python and Pandas, loads it into PostgreSQL, generates analytical visualizations, and orchestrates the complete workflow using Apache Airflow running in Docker.

## Project Overview

This project demonstrates a production-style ETL workflow for financial market data.

The pipeline performs the following operations:

1. Extracts daily stock market data from the Alpha Vantage REST API.
2. Converts the API JSON response into a structured Pandas DataFrame.
3. Cleans and validates financial data.
4. Converts columns into appropriate numeric and datetime data types.
5. Removes invalid and duplicate records.
6. Loads transformed data into PostgreSQL.
7. Prevents duplicate database records using idempotent inserts.
8. Generates financial data visualizations.
9. Orchestrates and schedules the complete pipeline using Apache Airflow.
10. Runs the Airflow environment using Docker Compose.

## Architecture

```text
                    Alpha Vantage API
                           |
                           v
                    Python Extraction
                           |
                           v
                    Pandas Transform
                           |
                           v
                     PostgreSQL
                           |
                           v
                Financial Visualizations

                           ^
                           |
                   Apache Airflow
                           |
                           v
                    Docker Compose
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core ETL development |
| Pandas | Data transformation and cleaning |
| Requests | REST API integration |
| PostgreSQL | Financial data storage |
| SQLAlchemy | Database connectivity |
| Matplotlib | Financial visualizations |
| Seaborn | Correlation heatmap |
| Apache Airflow | Workflow orchestration and scheduling |
| Docker | Containerized Airflow environment |
| Docker Compose | Multi-container orchestration |
| Alpha Vantage API | Financial market data source |

## Project Structure

```text
stock-etl-pipeline/
│
├── airflow/
│   ├── dags/
│   │   └── financial_etl_dag.py
│   ├── config/
│   └── plugins/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── logger.py
│   └── main.py
│
├── visualization/
│   ├── __init__.py
│   ├── charts.py
│   └── output/
│
├── sql/
│   └── create_tables.sql
│
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ETL Pipeline

### 1. Extract

The extraction layer retrieves daily stock market data from the Alpha Vantage API.

The API response contains daily:

- Open price
- High price
- Low price
- Close price
- Trading volume

API credentials are stored using environment variables rather than hardcoded into the application.

### 2. Transform

The transformation layer converts the raw JSON response into a clean Pandas DataFrame.

Transformations include:

- JSON-to-DataFrame conversion
- Column renaming
- Numeric type conversion
- Datetime conversion
- Date sorting
- Duplicate removal
- Null-value removal
- Financial field normalization

The final dataset contains:

```text
date
open_price
high_price
low_price
close_price
volume
```

### 3. Load

The transformed data is loaded into PostgreSQL using SQLAlchemy.

The database layer uses conflict handling to make repeated pipeline executions idempotent.

```sql
ON CONFLICT (trade_date)
DO NOTHING;
```

Therefore, rerunning the pipeline does not create duplicate records for dates already stored in the database.

## Data Visualizations

The pipeline automatically generates:

- Closing Price Line Chart
- Daily Trading Volume Chart
- 20-Day Moving Average Chart
- Closing Price Histogram
- Closing Price Box Plot
- Correlation Heatmap

Generated visualizations are stored in:

```text
visualization/output/
```

## Apache Airflow Orchestration

Apache Airflow orchestrates execution of the financial ETL pipeline.

DAG:

```text
financial_etl_pipeline
```

The DAG executes the Python ETL application and monitors its execution state.

The pipeline can be:

- Triggered manually from the Airflow UI
- Executed automatically according to its configured schedule
- Monitored through Airflow task logs
- Retried automatically when failures occur

The DAG is configured with retry handling so transient failures can be retried automatically.

## Scheduling

The DAG is configured to run daily at:

```text
22:00 Asia/Ho_Chi_Minh
```

Cron expression:

```text
0 22 * * *
```

Manual DAG runs can also be triggered at any time independently of the automatic schedule.

## Docker Architecture

Apache Airflow runs using Docker Compose.

The environment contains services such as:

```text
Airflow API Server
Airflow Scheduler
Airflow DAG Processor
Airflow Worker
Airflow Triggerer
PostgreSQL
Redis
```

The project source directory is bind-mounted into the Airflow containers so source-code changes can be used without manually copying files into containers.

## Environment Variables

Copy `.env.example` to `.env` as a template.

Example:

```env
ALPHA_VANTAGE_API_KEY=your_api_key
STOCK_SYMBOL=IBM

DB_HOST=host.docker.internal
DB_PORT=5432
DB_NAME=stock_market
DB_USER=postgres
DB_PASSWORD=your_password

AIRFLOW_UID=50000
FERNET_KEY=
```

The real `.env` file is excluded from Git using `.gitignore`.

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/Tomwakeupat530amm/stock-etl-pipeline.git
cd stock-etl-pipeline
```

### 2. Configure environment variables

Create `.env` from `.env.example` and provide the required credentials.

### 2b. Create the database table

Create the `stock_market` database in PostgreSQL, then run `sql/create_tables.sql` against it.

### 3. Initialize Airflow

```bash
docker compose up airflow-init
```

### 4. Start Airflow

```bash
docker compose up -d
```

### 5. Check container health

```bash
docker compose ps
```

### 6. Open Airflow

Open the Airflow web interface on port `8080`.

Find:

```text
financial_etl_pipeline
```

Enable the DAG and trigger it manually or allow the configured schedule to execute it.

### 7. Stop the environment

```bash
docker compose down
```

## Running the ETL Without Airflow

The ETL application can also be executed directly:

```bash
python -m src.main
```

This is useful for local development and debugging.

## Error Handling and Logging

The application uses structured logging throughout the ETL pipeline.

Failures during extraction, transformation, database loading, or visualization generation are propagated to Airflow so failed pipeline executions are correctly marked as failed.

Airflow additionally provides:

- Task execution logs
- DAG run history
- Retry handling
- Task state monitoring
- Failure visibility

## Key Data Engineering Concepts Demonstrated

This project demonstrates:

- ETL pipeline design
- REST API ingestion
- JSON processing
- Pandas transformations
- Data validation
- PostgreSQL persistence
- SQLAlchemy database integration
- Idempotent data loading
- Workflow orchestration
- DAG scheduling
- Retry and failure handling
- Environment-variable based configuration
- Containerization
- Docker Compose
- Logging and monitoring
- Financial data visualization

## Future Enhancements

Potential improvements include:

- Multi-stock ingestion
- Incremental API extraction
- Separate Airflow tasks for Extract, Transform, Load and visualization
- Airflow XCom usage
- Data quality validation tasks
- Stock symbol configuration
- Parallel stock processing
- Kafka-based streaming market data ingestion
- Redis caching
- TimescaleDB integration
- PySpark processing
- Cloud deployment
- CI/CD using GitHub Actions
- Prometheus and Grafana monitoring
- Automated tests with Pytest

## Disclaimer

This project is intended for educational and portfolio purposes. Market data provided by external APIs may be delayed or subject to provider limitations and should not be treated as investment advice.