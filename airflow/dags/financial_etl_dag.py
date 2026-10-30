from __future__ import annotations

import subprocess
from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


PROJECT_ROOT = "/opt/airflow/project"


def run_financial_etl() -> None:
    result = subprocess.run(
        ["python", "-m", "src.main"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.stdout:
        print("===== ETL OUTPUT =====")
        print(result.stdout)

    if result.stderr:
        print("===== ETL ERRORS =====")
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(
            f"Financial ETL failed with exit code {result.returncode}"
        )


default_args = {
    "owner": "tom",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


local_tz = pendulum.timezone("Asia/Ho_Chi_Minh")


with DAG(
    dag_id="financial_etl_pipeline",
    description=(
        "Extract stock data, transform it, load PostgreSQL, "
        "and generate analytical charts."
    ),
    default_args=default_args,
    start_date=pendulum.datetime(
        2026, 8, 1, 0, 0, tz=local_tz
    ),
    schedule="0 22 * * *",
    catchup=False,
    tags=["python", "etl", "stocks"],
) as dag:

    run_pipeline = PythonOperator(
        task_id="run_financial_etl",
        python_callable=run_financial_etl,
    )