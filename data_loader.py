import os

import numpy as np
import pandas as pd

import psycopg2 as psycopg
from dotenv import load_dotenv


def load_data():

    load_dotenv()

    connection = {"host": os.getenv("DB_DESTINATION_HOST"),
                'port': os.getenv("DB_DESTINATION_PORT"),
                "dbname": os.getenv("DB_DESTINATION_NAME"),
                "user": os.getenv("DB_DESTINATION_USER"),
                "password": os.getenv("DB_DESTINATION_PASSWORD"),
                'sslmode': 'require',
                'target_session_attrs': 'read-write'}

    TABLE_NAME = 'clean_dataset_build_price_2'

    with psycopg.connect(**connection) as conn:
        with conn.cursor() as cur:
            cur.execute(f'SELECT * FROM {TABLE_NAME}')
            data = cur.fetchall()
            columns = [col[0] for col in cur.description]

    data = pd.DataFrame(data, columns=columns)

    return data


def prepare_data():
    data = load_data()

    # логарифмируем и приводим к нужному виду датасет
    data['price'] = data['price'].astype('float')
    data['price'] = np.log1p(data['price'])
    
    os.makedirs('data', exist_ok=True)
    data.to_csv('data/dataset.csv', index=None)


if __name__ == "__main__":
    prepare_data()