FROM apache/airflow:3.3.0

USER airflow

RUN pip install --no-cache-dir \
    pandas \
    requests \
    python-dotenv \
    sqlalchemy \
    psycopg2-binary \
    matplotlib \
    seaborn