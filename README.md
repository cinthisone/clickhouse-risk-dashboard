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
├── data/          # Sample datasets and storage (not tracked in git)
├── scripts/       # ETL, analytics, and data download scripts
├── app/           # Streamlit web interface
├── requirements.txt
├── README.md
├── .gitignore
```

# (Private/local only, not in repo)
# ├── memory-bank/   # Project context and memory files
# ├── Inhouse-Notes-Clickhouse/   # Personal ClickHouse learning notes

## Usage

1. Data Ingestion:
```

## 🚀 Cloud & Docker Deployment (Recommended)

You can deploy this project on any cloud VM (Azure, GCP, AWS, etc.) using Docker for fast, reproducible setup.

### Quick Start on a New VM (Azure, East US, Ubuntu 22.04)

1. **Install Docker & Docker Compose:**
   ```bash
   sudo apt-get update
   sudo apt-get install docker.io docker-compose -y
   ```
2. **Clone the repo:**
   ```bash
   git clone https://github.com/cinthisone/clickhouse-risk-dashboard.git
   cd clickhouse-risk-dashboard
   ```
3. **Add the provided `docker-compose.yml` and `Dockerfile` if not present.**
4. **Start the stack:**
   ```bash
   docker-compose up -d
   ```
5. **Access your dashboard:**
   - Streamlit: `http://<your-vm-public-ip>:8501`
   - ClickHouse HTTP: `http://<your-vm-public-ip>:8123`

---

## Next Steps for Your New Azure VM

1. **Open ports 22 (SSH), 8123 (ClickHouse HTTP), 9000 (ClickHouse native), and 8501 (Streamlit) in the Azure Portal.**
2. **SSH into your VM using your private key.**
3. **Follow the Docker Quick Start steps above.**
4. **(Optional) Copy your data CSVs into the `data/` folder and re-run ingestion/analytics as needed.**
5. **Visit your public IP in a browser to see your dashboard!**

---

For detailed Docker instructions and troubleshooting, see `Inhouse-Notes-Clickhouse/docker-deployment.md`.