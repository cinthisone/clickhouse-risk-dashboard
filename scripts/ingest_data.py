#!/usr/bin/env python3
"""
Data ingestion script for loading financial data into ClickHouse.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Any

import clickhouse_connect
import pandas as pd
from dotenv import load_dotenv

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

class DataIngestion:
    def __init__(self):
        """Initialize the data ingestion class."""
        self.client = clickhouse_connect.get_client(
            host=os.getenv('CLICKHOUSE_HOST'),
            port=int(os.getenv('CLICKHOUSE_PORT')),
            username=os.getenv('CLICKHOUSE_USER'),
            password=os.getenv('CLICKHOUSE_PASSWORD'),
            database=os.getenv('CLICKHOUSE_DB')
        )

    def load_csv_data(self, file_path: str, symbol: str) -> pd.DataFrame:
        """
        Load data from a CSV file.
        
        Args:
            file_path: Path to the CSV file
            symbol: Symbol for the financial instrument
            
        Returns:
            DataFrame with the loaded data
        """
        # Read CSV, skipping problematic rows
        df = pd.read_csv(file_path, skiprows=[1])  # Skip the second row
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Add symbol and source
        df['symbol'] = symbol
        df['source'] = 'csv_import'
        
        return df

    def prepare_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Prepare data for insertion into ClickHouse.
        
        Args:
            df: DataFrame with the data
            
        Returns:
            List of dictionaries ready for insertion
        """
        records = []
        for _, row in df.iterrows():
            try:
                record = {
                    'timestamp': row['timestamp'],
                    'symbol': row['symbol'],
                    'open': float(row['open']),
                    'high': float(row['high']),
                    'low': float(row['low']),
                    'close': float(row['close']),
                    'volume': float(row['volume']),
                    'source': row['source']
                }
                records.append(record)
            except (ValueError, TypeError) as e:
                print(f"Warning: Skipping row due to error: {e}")
                continue
        return records

    def insert_data(self, records: List[Dict[str, Any]]) -> None:
        """
        Insert data into ClickHouse.
        
        Args:
            records: List of records to insert
        """
        if not records:
            print("No valid records to insert")
            return
        # Convert records (list of dicts) to list of lists in column order
        columns = ['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'volume', 'source']
        data = [[rec[col] for col in columns] for rec in records]
        print(f"Inserting {len(data)} records. Sample record:")
        print(data[0] if data else 'No records')
        print(f"Type of first record: {type(data[0]) if data else 'N/A'}")
        self.client.insert(
            'financial_data.price_data',
            data,
            column_names=columns
        )

    def process_file(self, file_path: str, symbol: str) -> None:
        """
        Process a single data file.
        
        Args:
            file_path: Path to the data file
            symbol: Symbol for the financial instrument
        """
        print(f"Processing {file_path} for {symbol}")
        try:
            df = self.load_csv_data(file_path, symbol)
            records = self.prepare_data(df)
            self.insert_data(records)
            print(f"Successfully processed {len(records)} records")
        except Exception as e:
            import traceback
            print(f"Error processing file: {e}")
            traceback.print_exc()

def main():
    """Main function to run the data ingestion process."""
    ingestion = DataIngestion()
    
    # Example usage
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    
    # Process all CSV files in the data directory
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(data_dir, file_name)
            symbol = os.path.splitext(file_name)[0]  # Use filename as symbol
            ingestion.process_file(file_path, symbol)

if __name__ == '__main__':
    main() 