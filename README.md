# Risk Analytics System with ClickHouse

A self-hosted risk analytics system built on ClickHouse that demonstrates practical implementation of financial data analysis, risk metrics calculation, and visualization capabilities.

## Features

- Local ClickHouse server running in WSL
- Time-series financial data analysis
- Risk metric calculations (volatility, drawdown, Sharpe ratio)
- Data visualization with Matplotlib/Plotly
- Optional Streamlit web interface

## Prerequisites

- WSL2 with Ubuntu
- Python 3.8+
- Minimum 4GB RAM
- 20GB free disk space

## Installation

1. Install ClickHouse:
```bash
# Add ClickHouse repository
sudo apt-get install apt-transport-https ca-certificates dirmngr
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754
echo "deb https://packages.clickhouse.com/deb stable main" | sudo tee /etc/apt/sources.list.d/clickhouse.list
sudo apt-get update

# Install ClickHouse
sudo apt-get install clickhouse-server clickhouse-client
```

2. Set up Python environment:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. Start ClickHouse server:
```bash
sudo service clickhouse-server start
```

## Project Structure

```
/
├── sql/           # Schema definitions and queries
├── data/          # Sample datasets and storage
├── scripts/       # ETL and analytics scripts
├── app/           # Optional web interface
└── memory-bank/   # Project documentation
```

## Usage

1. Data Ingestion:
```bash
python scripts/ingest_data.py
```

2. Run Analytics:
```bash
python scripts/calculate_metrics.py
```

3. Launch Web Interface (Optional):
```bash
streamlit run app/main.py
```

## Development

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Use type hints in Python code

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 