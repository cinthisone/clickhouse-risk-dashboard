#!/usr/bin/env python3
"""
Download historical price data from Yahoo Finance using yfinance.
Saves the data as a CSV in the data/ directory.

Usage:
    python scripts/download_data.py --symbol BTC-USD --start 2023-01-01 --end 2024-01-01
"""
import os
import argparse
import yfinance as yf


def main():
    parser = argparse.ArgumentParser(description="Download historical price data from Yahoo Finance.")
    parser.add_argument('--symbol', type=str, required=True, help='Ticker symbol, e.g. BTC-USD or AAPL')
    parser.add_argument('--start', type=str, required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, required=True, help='End date (YYYY-MM-DD)')
    args = parser.parse_args()

    print(f"Downloading {args.symbol} from {args.start} to {args.end}...")
    df = yf.download(args.symbol, start=args.start, end=args.end)
    if df.empty:
        print("No data found. Check the symbol and date range.")
        return

    # Reset index to get 'Date' as a column
    df = df.reset_index()
    # Rename columns to match project schema
    df = df.rename(columns={
        'Date': 'timestamp',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    })
    # Only keep required columns
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, f"{args.symbol}.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved to {out_path}")

if __name__ == '__main__':
    main() 