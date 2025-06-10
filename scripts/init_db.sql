-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS financial_data;

-- Use the database
USE financial_data;

-- Create price_data table if it doesn't exist
CREATE TABLE IF NOT EXISTS price_data (
    timestamp DateTime,
    symbol String,
    open Float64,
    high Float64,
    low Float64,
    close Float64,
    volume Float64,
    source String
) ENGINE = MergeTree()
ORDER BY (timestamp, symbol);

-- Create risk_metrics table if it doesn't exist
CREATE TABLE IF NOT EXISTS risk_metrics (
    timestamp DateTime,
    symbol String,
    metric_name String,
    metric_value Float64
) ENGINE = MergeTree()
ORDER BY (timestamp, symbol, metric_name); 