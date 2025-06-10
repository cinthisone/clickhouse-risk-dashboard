# 🧠 Risk Dashboard with ClickHouse

This project is a high-performance, self-hosted risk analytics dashboard built using **ClickHouse** and **Streamlit**. It showcases time-series risk metrics such as **volatility**, **drawdown**, and **Sharpe ratio** for BTC-USD using real historical data.

> 📍 Built in WSL (Linux) using a local ClickHouse instance to simulate scalable backend data infrastructure.

---

## 🚀 Features

- ✅ Time-series ingestion into **ClickHouse**
- ✅ Lightning-fast querying using `clickhouse-connect`
- ✅ Interactive dashboard via **Streamlit**
- ✅ Candlestick charts and computed metrics:
  - Volatility (rolling std dev)
  - Drawdown
  - Sharpe Ratio
- ✅ Adjustable date range & symbol selection
- ✅ UI designed for readability and quant use

---

## 📦 Tech Stack

| Layer         | Tools Used                          |
|---------------|-------------------------------------|
| Backend DB    | ClickHouse (self-hosted in WSL)     |
| Data Ingest   | Python + `clickhouse-connect`       |
| Analytics     | Pandas, NumPy, Matplotlib           |
| Frontend/UI   | Streamlit                           |

---

## 🧠 Why I Built This

I created this project to gain hands-on experience with **ClickHouse**, time-series analytics, and financial risk metrics. It also allowed me to practice first-principles learning by building a fully functional tool while learning the tech along the way.

> It reflects my goal of working in a quantitative development or risk engineering role where data performance, model visibility, and financial insight intersect.

---

## 🔗 Demo & Source

- 📺 [Live Demo (Hosted)](https://quant.inthisone.com/projects/risk-dashboard)  
- 💻 [GitHub Source](https://github.com/cinthisone/clickhouse-risk-dashboard)

---

## 🛠️ Setup Guide

Coming soon — I'll publish a step-by-step guide for setting up ClickHouse in WSL and connecting it with Python/Streamlit.

---

# Inhouse Notes: ClickHouse

Welcome to your personal ClickHouse learning notes! This folder is for your reference as you explore and master ClickHouse.

---

## What is ClickHouse?
ClickHouse is a fast, open-source, column-oriented database management system (DBMS) for online analytical processing (OLAP). It's designed for real-time analytics on large volumes of data.

---

## Key Concepts
- **Columnar Storage:** Data is stored by columns, not rows. This makes analytical queries much faster.
- **OLAP:** Optimized for analytical queries (aggregations, time-series, etc.), not transactional workloads.
- **MergeTree Engine:** The most common table engine, supports fast inserts and queries, partitioning, and primary keys.
- **Materialized Views:** Precompute and store query results for fast access.

---

## Basic ClickHouse CLI Commands

- **Start the client:**
  ```bash
  clickhouse-client
  ```
- **Show databases:**
  ```sql
  SHOW DATABASES;
  ```
- **Use a database:**
  ```sql
  USE financial_data;
  ```
- **Show tables:**
  ```sql
  SHOW TABLES;
  ```
- **Describe a table:**
  ```sql
  DESCRIBE TABLE price_data;
  ```
- **Query data:**
  ```sql
  SELECT * FROM price_data LIMIT 10;
  ```
- **Count rows:**
  ```sql
  SELECT COUNT(*) FROM price_data;
  ```

---

## Useful SQL Patterns
- **Filter by date:**
  ```sql
  SELECT * FROM price_data WHERE timestamp >= '2023-01-01' AND timestamp < '2024-01-01';
  ```
- **Aggregate (e.g., daily average):**
  ```sql
  SELECT toDate(timestamp) AS day, avg(close) AS avg_close
  FROM price_data
  GROUP BY day
  ORDER BY day;
  ```
- **Get distinct symbols:**
  ```sql
  SELECT DISTINCT symbol FROM price_data;
  ```

---

## Resources
- [ClickHouse Official Docs](https://clickhouse.com/docs/en/)
- [ClickHouse Playground (try online)](https://play.clickhouse.com/)
- [ClickHouse SQL Reference](https://clickhouse.com/docs/en/sql-reference/)
- [Awesome ClickHouse (community resources)](https://github.com/ClickHouse/awesome-clickhouse)

---

## Tips
- ClickHouse is case-insensitive for SQL keywords, but case-sensitive for table/column names.
- Use `LIMIT` when exploring data to avoid huge result sets.
- Partitioning and primary keys are important for performance—read about `MergeTree` settings.
- You can use HTTP, native, or JDBC/ODBC clients to connect.

---

Happy learning! Add your own notes and questions here as you go. 