CREATE TABLE IF NOT EXISTS daily_stock_prices (

    trade_date DATE PRIMARY KEY,

    open_price NUMERIC(10,2) NOT NULL,

    high_price NUMERIC(10,2) NOT NULL,

    low_price NUMERIC(10,2) NOT NULL,

    close_price NUMERIC(10,2) NOT NULL,

    volume BIGINT NOT NULL

);