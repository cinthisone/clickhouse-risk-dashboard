#!/usr/bin/env python3
"""
Script for calculating risk metrics from financial data.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any

import clickhouse_connect
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

class RiskMetrics:
    def __init__(self):
        """Initialize the risk metrics calculator."""
        self.client = clickhouse_connect.get_client(
            host=os.getenv('CLICKHOUSE_HOST'),
            port=int(os.getenv('CLICKHOUSE_PORT')),
            username=os.getenv('CLICKHOUSE_USER'),
            password=os.getenv('CLICKHOUSE_PASSWORD'),
            database=os.getenv('CLICKHOUSE_DB')
        )

    def get_price_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Retrieve price data from ClickHouse.
        
        Args:
            symbol: Symbol to get data for
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with price data
        """
        query = """
        SELECT
            timestamp,
            symbol,
            close
        FROM financial_data.price_data
        WHERE symbol = %(symbol)s
        AND timestamp BETWEEN %(start_date)s AND %(end_date)s
        ORDER BY timestamp
        """
        
        result = self.client.query(
            query,
            parameters={
                'symbol': symbol,
                'start_date': start_date,
                'end_date': end_date
            }
        )
        
        return pd.DataFrame(result.result_rows, columns=['timestamp', 'symbol', 'close'])

    def calculate_volatility(self, df: pd.DataFrame, window: int = 20) -> pd.Series:
        """
        Calculate rolling volatility.
        
        Args:
            df: DataFrame with price data
            window: Rolling window size in days
            
        Returns:
            Series with volatility values
        """
        returns = df['close'].pct_change()
        return returns.rolling(window=window).std() * np.sqrt(252)

    def calculate_drawdown(self, df: pd.DataFrame) -> pd.Series:
        """
        Calculate drawdown series.
        
        Args:
            df: DataFrame with price data
            
        Returns:
            Series with drawdown values
        """
        rolling_max = df['close'].expanding().max()
        drawdown = (df['close'] - rolling_max) / rolling_max
        return drawdown

    def calculate_sharpe_ratio(self, df: pd.DataFrame, window: int = 20, risk_free_rate: float = 0.02) -> pd.Series:
        """
        Calculate rolling Sharpe ratio.
        
        Args:
            df: DataFrame with price data
            window: Rolling window size in days
            risk_free_rate: Annual risk-free rate
            
        Returns:
            Series with Sharpe ratio values
        """
        returns = df['close'].pct_change()
        excess_returns = returns - risk_free_rate/252
        return (excess_returns.rolling(window=window).mean() * np.sqrt(252)) / \
               (returns.rolling(window=window).std() * np.sqrt(252))

    def save_metrics(self, metrics: List[Dict[str, Any]]) -> None:
        """
        Save calculated metrics to ClickHouse.
        
        Args:
            metrics: List of metric records to save
        """
        if not metrics:
            print("No metrics to save.")
            return
        columns = ['timestamp', 'symbol', 'metric_name', 'metric_value', 'window_size', 'calculation_date']
        data = [[m[col] for col in columns] for m in metrics]
        print(f"Inserting {len(data)} metrics. Sample: {data[0] if data else 'No data'}")
        self.client.insert(
            'risk_metrics',
            data,
            column_names=columns
        )

    def process_symbol(self, symbol: str, start_date: str, end_date: str) -> None:
        """
        Process a single symbol and calculate all metrics.
        
        Args:
            symbol: Symbol to process
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        """
        print(f"Processing {symbol}")
        
        # Get price data
        df = self.get_price_data(symbol, start_date, end_date)
        if df.empty:
            print(f"No data found for {symbol}")
            return

        # Calculate metrics
        volatility = self.calculate_volatility(df)
        drawdown = self.calculate_drawdown(df)
        sharpe = self.calculate_sharpe_ratio(df)

        # Prepare metrics for saving
        metrics = []
        calculation_date = datetime.now()

        for timestamp, vol, dd, shrp in zip(df['timestamp'], volatility, drawdown, sharpe):
            if not np.isnan(vol):
                metrics.append({
                    'timestamp': timestamp,
                    'symbol': symbol,
                    'metric_name': 'volatility',
                    'metric_value': float(vol),
                    'window_size': 20,
                    'calculation_date': calculation_date
                })
            
            if not np.isnan(dd):
                metrics.append({
                    'timestamp': timestamp,
                    'symbol': symbol,
                    'metric_name': 'drawdown',
                    'metric_value': float(dd),
                    'window_size': 0,
                    'calculation_date': calculation_date
                })
            
            if not np.isnan(shrp):
                metrics.append({
                    'timestamp': timestamp,
                    'symbol': symbol,
                    'metric_name': 'sharpe_ratio',
                    'metric_value': float(shrp),
                    'window_size': 20,
                    'calculation_date': calculation_date
                })

        # Save metrics
        if metrics:
            self.save_metrics(metrics)
            print(f"Saved {len(metrics)} metrics for {symbol}")

def main():
    """Main function to run the risk metrics calculation process."""
    calculator = RiskMetrics()
    
    # Example usage
    symbols = ['BTC-USD', 'ETH-USD']  # Example symbols
    start_date = '2023-01-01'
    end_date = '2023-12-31'
    
    for symbol in symbols:
        calculator.process_symbol(symbol, start_date, end_date)

if __name__ == '__main__':
    main() 