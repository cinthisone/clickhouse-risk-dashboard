-- Create database for financial data
CREATE DATABASE IF NOT EXISTS financial_data;

-- Create table for price data
CREATE TABLE IF NOT EXISTS financial_data.price_data
(
    timestamp DateTime,
    symbol String,
    open Float64,
    high Float64,
    low Float64,
    close Float64,
    volume Float64,
    source String
)
ENGINE = MergeTree()
ORDER BY (symbol, timestamp)
PARTITION BY toYYYYMM(timestamp);

-- Create table for calculated metrics
CREATE TABLE IF NOT EXISTS financial_data.risk_metrics
(
    timestamp DateTime,
    symbol String,
    metric_name String,
    metric_value Float64,
    window_size UInt32,
    calculation_date DateTime
)
ENGINE = MergeTree()
ORDER BY (symbol, metric_name, timestamp)
PARTITION BY toYYYYMM(timestamp);

-- Create materialized view for daily returns
CREATE MATERIALIZED VIEW IF NOT EXISTS financial_data.daily_returns
ENGINE = MergeTree()
ORDER BY (symbol, timestamp)
PARTITION BY toYYYYMM(timestamp)
AS
SELECT
    timestamp,
    symbol,
    (close - lagInFrame(close) OVER (PARTITION BY symbol ORDER BY timestamp)) / 
    lagInFrame(close) OVER (PARTITION BY symbol ORDER BY timestamp) as daily_return
FROM financial_data.price_data;

-- Create materialized view for volatility
CREATE MATERIALIZED VIEW IF NOT EXISTS financial_data.volatility
ENGINE = MergeTree()
ORDER BY (symbol, timestamp)
PARTITION BY toYYYYMM(timestamp)
AS
SELECT
    timestamp,
    symbol,
    stddevSamp(daily_return) OVER (
        PARTITION BY symbol 
        ORDER BY timestamp 
        RANGE BETWEEN 20 PRECEDING AND CURRENT ROW
    ) * sqrt(252) as volatility_20d
FROM financial_data.daily_returns; 