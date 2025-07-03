import pandas as pd
import logging

def clean_data(df):
    logging.info("Cleaning data")
    df = df.dropna()
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    # Example: Aggregate sales by month if columns exist
    return df