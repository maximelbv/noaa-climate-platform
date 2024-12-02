import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_NAME = "noaa"
RAW_DATA_DIR = "./data/raw"

DATASETS = {
    "gsod": {
        "folder": "gsod",
        "table": "gsod_data"
    },
    "isd": {
        "folder": "isd",
        "table": "isd_data"
    }
}

def connect_to_postgres():
    """Connect to PostgreSQL and return the connection object."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

def load_csv_to_postgres(dataset_name, table_name):
    """Load a CSV file into PostgreSQL table."""
    dataset_dir = os.path.join(RAW_DATA_DIR, dataset_name)
    for year in os.listdir(dataset_dir):
        year_dir = os.path.join(dataset_dir, year)
        for file_name in os.listdir(year_dir):
            if file_name.endswith('.csv'):
                file_path = os.path.join(year_dir, file_name)
                print(f"[INFO] Loading {file_path} into {table_name}...")
                df = pd.read_csv(file_path)
                
                # Create connection to the PostgreSQL database
                conn = connect_to_postgres()
                engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
                
                try:
                    df.to_sql(table_name, engine, if_exists="append", index=False)
                    print(f"[INFO] Successfully loaded {file_name} into {table_name}")
                except Exception as e:
                    print(f"[ERROR] Failed to load {file_name} into {table_name}: {e}")
                finally:
                    conn.close()

def ingest():
    """Main function to ingest all datasets."""
    for dataset_name, info in DATASETS.items():
        load_csv_to_postgres(dataset_name, info["table"])

if __name__ == "__main__":
    ingest()
