import sys
import os

# Add the parent directory of 'dags' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging
import yaml
from etl.extract import download_data, load_csv
from etl.transform import clean_data
from etl.load import load_to_postgres

def load_config():
    with open('/Users/ayushupadhyay/Documents/GitHub/end_to_end_ETL/config/config.yaml') as f:
        return yaml.safe_load(f)

def etl():
    config = load_config()
    download_data(config)
    df = load_csv(config)
    df_clean = clean_data(df)
    load_to_postgres(df_clean, config)

with DAG('warehouse_sales_etl', start_date=datetime(2025, 6,30 ), schedule = None, catchup=False) as dag:
    etl_task = PythonOperator(
        task_id='run_etl',
        python_callable=etl
    )
