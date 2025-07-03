import requests
import logging
import pandas as pd
import yaml

def download_data(config):
    url = config['data_url']
    output_path = config['raw_data_path']
    logging.info(f"Downloading data from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
    logging.info(f"Data saved to {output_path}")

def load_csv(config):
    path = config['raw_data_path']
    logging.info(f"Loading CSV from {path}")
    return pd.read_csv(path)

