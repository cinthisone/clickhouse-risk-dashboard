# Risk Analytics System with ClickHouse

## Project Overview
A self-hosted risk analytics system built on ClickHouse that demonstrates practical implementation of financial data analysis, risk metrics calculation, and visualization capabilities.

## Core Requirements

### 1. Infrastructure
- ClickHouse server running locally in WSL (Ubuntu)
- Python environment with required packages
- Optional web interface using Streamlit

### 2. Data Management
- Schema design for time-series financial data
- ETL pipeline for data ingestion and updates
- Support for public financial datasets (crypto/equities)

### 3. Analytics Capabilities
- Risk metric calculations:
  - Volatility
  - Drawdown analysis
  - Rolling Sharpe ratio
  - Other relevant risk metrics
- Data visualization using Matplotlib/Plotly
- Interactive dashboards (optional)

### 4. Project Structure
```
/
├── sql/           # Schema definitions and queries
├── data/          # Sample datasets and storage
├── scripts/       # ETL and analytics scripts
├── app/           # Optional web interface
└── memory-bank/   # Project documentation
```

## Success Criteria
1. Functional ClickHouse instance running in WSL
2. Successful data ingestion pipeline
3. Accurate risk metric calculations
4. Clear visualizations of results
5. Well-documented codebase
6. Optional: Interactive web interface

## Technical Constraints
- Must run entirely locally in WSL
- Should use public datasets for demonstration
- Must maintain good performance with reasonable data volumes
- Should follow Python best practices and code organization

## Project Goals
1. Demonstrate backend development skills
2. Showcase data pipeline implementation
3. Implement complex risk calculations
4. Display understanding of distributed systems
5. Create a maintainable and extensible codebase 