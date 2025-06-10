#!/usr/bin/env python3
"""
Streamlit application for visualizing financial data and risk metrics.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Optional

import clickhouse_connect
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

class FinancialVisualizer:
    def __init__(self):
        """Initialize the financial visualizer."""
        self.client = clickhouse_connect.get_client(
            host='localhost',
            port=8123,
            username='default',
            password=''
        )

    def get_available_symbols(self) -> List[str]:
        """Get list of available symbols."""
        query = "SELECT DISTINCT symbol FROM financial_data.price_data"
        result = self.client.query(query)
        return [row[0] for row in result.result_rows]

    def get_price_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get price data for a symbol."""
        query = """
        SELECT
            timestamp,
            symbol,
            open,
            high,
            low,
            close,
            volume
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
        
        return pd.DataFrame(
            result.result_rows,
            columns=['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'volume']
        )

    def get_risk_metrics(self, symbol: str, metric_name: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get risk metrics for a symbol."""
        query = """
        SELECT
            timestamp,
            metric_value
        FROM financial_data.risk_metrics
        WHERE symbol = %(symbol)s
        AND metric_name = %(metric_name)s
        AND timestamp BETWEEN %(start_date)s AND %(end_date)s
        ORDER BY timestamp
        """
        
        result = self.client.query(
            query,
            parameters={
                'symbol': symbol,
                'metric_name': metric_name,
                'start_date': start_date,
                'end_date': end_date
            }
        )
        
        return pd.DataFrame(result.result_rows, columns=['timestamp', 'value'])

    def plot_price_data(self, df: pd.DataFrame) -> go.Figure:
        """Create price chart."""
        fig = go.Figure()
        
        fig.add_trace(go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        ))
        
        fig.update_layout(
            title='Price Chart',
            yaxis_title='Price',
            xaxis_title='Date',
            template='plotly_dark'
        )
        
        return fig

    def plot_metric(self, df: pd.DataFrame, metric_name: str) -> go.Figure:
        """Create metric chart."""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['value'],
            name=metric_name
        ))
        
        fig.update_layout(
            title=f'{metric_name.title()} Chart',
            yaxis_title=metric_name.title(),
            xaxis_title='Date',
            template='plotly_dark'
        )
        
        return fig

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title='Financial Analytics', layout='wide')
    
    st.title('Financial Analytics Dashboard')
    
    # Initialize visualizer
    visualizer = FinancialVisualizer()
    
    # Get available symbols
    symbols = visualizer.get_available_symbols()
    
    # Sidebar controls
    st.sidebar.header('Controls')
    
    symbol = st.sidebar.selectbox('Select Symbol', symbols)
    
    # Date range selection
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    date_range = st.sidebar.date_input(
        'Select Date Range',
        value=(start_date, end_date),
        max_value=end_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.error('Please select a date range')
        return
    
    # Get data
    price_data = visualizer.get_price_data(
        symbol,
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )
    
    # Display price chart
    st.subheader('Price Chart')
    price_fig = visualizer.plot_price_data(price_data)
    st.plotly_chart(price_fig, use_container_width=True)
    
    # Display risk metrics
    st.subheader('Risk Metrics')
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        volatility_data = visualizer.get_risk_metrics(
            symbol,
            'volatility',
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        if not volatility_data.empty:
            vol_fig = visualizer.plot_metric(volatility_data, 'Volatility')
            st.plotly_chart(vol_fig, use_container_width=True)
    
    with col2:
        drawdown_data = visualizer.get_risk_metrics(
            symbol,
            'drawdown',
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        if not drawdown_data.empty:
            dd_fig = visualizer.plot_metric(drawdown_data, 'Drawdown')
            st.plotly_chart(dd_fig, use_container_width=True)
    
    with col3:
        sharpe_data = visualizer.get_risk_metrics(
            symbol,
            'sharpe_ratio',
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        if not sharpe_data.empty:
            sharpe_fig = visualizer.plot_metric(sharpe_data, 'Sharpe Ratio')
            st.plotly_chart(sharpe_fig, use_container_width=True)

if __name__ == '__main__':
    main() 