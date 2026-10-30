from src.extract import extract_stock_data
from src.transform import transform_stock_data
from src.load import load_to_postgres
from src.logger import logger

from visualization.charts import (
    create_closing_price_chart,
    create_volume_chart,
    create_moving_average_chart,
    create_histogram,
    create_boxplot,
    create_correlation_heatmap,
)


def main():

    logger.info("ETL Pipeline Started")

    try:
        raw_data = extract_stock_data()
        logger.info("Data Extracted Successfully")

        df = transform_stock_data(raw_data)
        logger.info("Data Transformed Successfully")

        load_to_postgres(df)
        logger.info("Data Loaded Successfully")

        create_closing_price_chart(df)
        create_volume_chart(df)
        create_moving_average_chart(df)
        create_histogram(df)
        create_boxplot(df)
        create_correlation_heatmap(df)

        logger.info("Charts Generated Successfully")
        logger.info("ETL Pipeline Finished Successfully")

    except Exception as e:
        logger.exception(f"ETL Pipeline Failed: {e}")
        raise


if __name__ == "__main__":
    main()