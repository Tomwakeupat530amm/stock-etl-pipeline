CREATE TABLE IF NOT EXISTS daily_stock_prices (
    symbol        VARCHAR(10)   NOT NULL,
    trade_date    DATE          NOT NULL,
    open_price    NUMERIC(12,2) NOT NULL,
    high_price    NUMERIC(12,2) NOT NULL,
    low_price     NUMERIC(12,2) NOT NULL,
    close_price   NUMERIC(12,2) NOT NULL,
    volume        BIGINT        NOT NULL,
    daily_return  NUMERIC(10,4),
    PRIMARY KEY (symbol, trade_date)
);
