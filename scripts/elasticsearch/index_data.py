import requests
import json
import os
import csv
from pymongo import MongoClient

# Configuration for Elasticsearch
ES_HOST = "localhost"
ES_PORT = 9200
ES_SCHEME = "http"
ES_INDEX = "mongo_storm_events_data"

# MongoDB Configuration
MONGO_URI = "mongodb://admin:password@localhost:27017/"
DATABASE_NAME = "noaa"
RAW_DATA_DIR = "./data/raw"

DATASETS = {
    "storm_events": {
        "folder": "storm_events",
        "collection": "storm_events"
    },
}

# Connect to MongoDB
def connect_to_mongo():
    """Connect to MongoDB and return the client."""
    return MongoClient(MONGO_URI)

# Create Elasticsearch index with mappings
def create_index_with_mappings():
    """Create Elasticsearch index with predefined mappings."""
    mappings = {
        "mappings": {
            "properties": {
                "STATE": {
                    "type": "keyword"
                },
                "EVENT_TYPE": {
                    "type": "keyword"
                },
                "CZ_NAME": {
                    "type": "keyword"
                },
                "WFO": {
                    "type": "keyword"
                },
                "BEGIN_DATE_TIME": {
                    "type": "date",
                    "format": "dd-MMM-yy HH:mm:ss"
                },
                "END_DATE_TIME": {
                    "type": "date",
                    "format": "dd-MMM-yy HH:mm:ss"
                },
                "INJURIES_DIRECT": {
                    "type": "integer"
                },
                "INJURIES_INDIRECT": {
                    "type": "integer"
                },
                "DEATHS_DIRECT": {
                    "type": "integer"
                },
                "DEATHS_INDIRECT": {
                    "type": "integer"
                },
                "DAMAGE_PROPERTY": {
                    "type": "float"
                },
                "DAMAGE_CROPS": {
                    "type": "float"
                },
                "MAGNITUDE": {
                    "type": "float"
                },
                "MAGNITUDE_TYPE": {
                    "type": "keyword"
                },
                "FLOOD_CAUSE": {
                    "type": "text"
                },
                "CATEGORY": {
                    "type": "keyword"
                },
                "TOR_F_SCALE": {
                    "type": "keyword"
                },
                "TOR_LENGTH": {
                    "type": "float"
                },
                "TOR_WIDTH": {
                    "type": "float"
                },
                "TOR_OTHER_WFO": {
                    "type": "keyword"
                },
                "TOR_OTHER_CZ_STATE": {
                    "type": "keyword"
                },
                "TOR_OTHER_CZ_FIPS": {
                    "type": "keyword"
                },
                "TOR_OTHER_CZ_NAME": {
                    "type": "keyword"
                },
                "BEGIN_LAT": {
                    "type": "float"
                },
                "BEGIN_LON": {
                    "type": "float"
                },
                "END_LAT": {
                    "type": "float"
                },
                "END_LON": {
                    "type": "float"
                },
                "EPISODE_NARRATIVE": {
                    "type": "text"
                },
                "EVENT_NARRATIVE": {
                    "type": "text"
                },
                "DATA_SOURCE": {
                    "type": "keyword"
                }
            }
        }
    }

    url = f"{ES_SCHEME}://{ES_HOST}:{ES_PORT}/{ES_INDEX}"
    
    # Check if the index exists
    response = requests.get(url)
    
    if response.status_code == 404:  # Index does not exist
        # Create index with mappings
        response = requests.put(url, json=mappings)
        if response.status_code == 200:
            print(f"[INFO] Successfully created index: {ES_INDEX}")
        else:
            print(f"[ERROR] Failed to create index: {response.text}")
    else:
        print(f"[INFO] Index {ES_INDEX} already exists.")

# Function to index data into Elasticsearch using requests
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

# Function to process MongoDB data and index it in Elasticsearch
def process_mongo_data(dataset_name):
    """Process and index MongoDB data."""
    client = connect_to_mongo()
    db = client[DATABASE_NAME]
    collection = db[dataset_name]
    
    for document in collection.find():
        try:
            index_with_requests(document)
        except Exception as e:
            print(f"[ERROR] Failed to index document: {e}")

# Function to index CSV files into Elasticsearch
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

# Main function to process all datasets and index them to Elasticsearch
def main():
    """Main function to process and index all datasets."""
    
    # Step 1: Create index with mappings
    create_index_with_mappings()
    
    # Step 2: Process MongoDB data
    print("[INFO] Starting MongoDB data indexing...")
    for dataset_name, info in DATASETS.items():
        process_mongo_data(info["collection"])
    
    # Step 3: Index CSV data
    print("[INFO] Starting CSV data indexing...")
    for dataset_name, info in DATASETS.items():
        index_csv_to_es(dataset_name)

if __name__ == "__main__":
    main()
