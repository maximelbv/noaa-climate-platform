import requests
import json
import os
import csv
from pymongo import MongoClient

# Configuration pour Elasticsearch
ES_HOST = "localhost"
ES_PORT = 9200
ES_SCHEME = "http"
ES_INDEX = "mongo_storm_events_data"

# Connexion à MongoDB
MONGO_URI = "mongodb://admin:password@localhost:27017/"
DATABASE_NAME = "noaa"
RAW_DATA_DIR = "./data/raw"

DATASETS = {
    "storm_events": {
        "folder": "storm_events",
        "collection": "storm_events"
    },
}

# Connexion à MongoDB
def connect_to_mongo():
    """Connect to MongoDB and return the client."""
    return MongoClient(MONGO_URI)

# Fonction pour indexer les données avec requests
def index_with_requests(data):
    """Index data into Elasticsearch using requests."""
    url = f"http://{ES_HOST}:{ES_PORT}/{ES_INDEX}/_doc/"
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"[INFO] Successfully indexed data: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error indexing data: {e}")

# Fonction pour transformer les données de MongoDB et les indexer dans Elasticsearch
def process_mongo_data(dataset_name):
    """Process and index the MongoDB data."""
    client = connect_to_mongo()
    db = client[DATABASE_NAME]
    collection = db[dataset_name]
    
    for document in collection.find():
        try:
            index_with_requests(document)
        except Exception as e:
            print(f"[ERROR] Failed to index document: {e}")

# Fonction pour indexer les fichiers CSV dans Elasticsearch
def index_csv_to_es(dataset_name):
    """Load and index CSV files into Elasticsearch."""
    dataset_dir = os.path.join(RAW_DATA_DIR, dataset_name)
    
    for file_name in os.listdir(dataset_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(dataset_dir, file_name)
            print(f"[INFO] Loading {file_path} into Elasticsearch...")
            
            with open(file_path, newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        index_with_requests(row)
                    except Exception as e:
                        print(f"[ERROR] Failed to index row: {e}")

# Fonction principale pour indexer les données
def main():
    """Main function to process all datasets and index to Elasticsearch."""
    print("[INFO] Starting MongoDB data indexing...")
    for dataset_name, info in DATASETS.items():
        process_mongo_data(info["collection"])
    
    print("[INFO] Starting CSV data indexing...")
    for dataset_name, info in DATASETS.items():
        index_csv_to_es(dataset_name)

if __name__ == "__main__":
    main()
