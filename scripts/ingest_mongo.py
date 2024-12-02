import os
import csv
import pandas as pd
from pymongo import MongoClient

MONGO_URI = "mongodb://admin:password@localhost:27017/"
DATABASE_NAME = "noaa"
RAW_DATA_DIR = "./data/raw"

DATASETS = {
    "storm_events": {
        "folder": "storm_events",
        "collection": "storm_events"
    },
    "metar": {
        "folder": "metar",
        "collection": "metar"
    }
}

def connect_to_mongo():
    """Connect to MongoDB and return the client."""
    return MongoClient(MONGO_URI)

def process_row(row, dataset_name):
    """Process and clean the row data before inserting."""
    if row:  # Check if row is not None or empty
        if dataset_name == "storm_events":
            row["event_type"] = row.get("event_type", "").strip()
            row["location"] = row.get("location", "").strip()
            row["date"] = row.get("date", "").strip()
        elif dataset_name == "metar":
            pass  # Process METAR data if needed
        return row
    return None  # Return None if the row is empty or invalid

def map_reduce_simulation(dataset_name, file_path):
    """Simulate MapReduce with Pandas on the loaded data."""
    # Read the CSV into a Pandas DataFrame
    df = pd.read_csv(file_path)
    
    if dataset_name == "storm_events":
        # Map step: Select relevant columns (example: 'station_id' and 'temperature')
        mapped_data = df[['station_id', 'temperature']]
        
        # Reduce step: Aggregate data (example: average temperature per station)
        reduced_data = mapped_data.groupby('station_id').agg({'temperature': 'mean'}).reset_index()

        # Insert the reduced data back to MongoDB
        client = connect_to_mongo()
        db = client[DATABASE_NAME]
        collection = db[dataset_name]
        
        # Convert DataFrame to dictionary for MongoDB insertion
        documents = reduced_data.to_dict(orient='records')
        
        if documents:
            try:
                collection.insert_many(documents)
                print(f"[INFO] Successfully inserted reduced data into {dataset_name}")
            except Exception as e:
                print(f"[ERROR] Failed to insert reduced data into {dataset_name}: {e}")
        client.close()

def load_csv_to_mongo(dataset_name, collection_name):
    """Load a CSV file into MongoDB collection."""
    dataset_dir = os.path.join(RAW_DATA_DIR, dataset_name)
    client = connect_to_mongo()
    db = client[DATABASE_NAME]
    collection = db[collection_name]

    for file_name in os.listdir(dataset_dir):
        if file_name.endswith('.csv'):  # Handle standard CSV files
            file_path = os.path.join(dataset_dir, file_name)
            print(f"[INFO] Loading {file_path} into {collection_name}...")
            
            with open(file_path, newline='') as f:
                reader = csv.DictReader(f)
                documents = []
                for row in reader:
                    try:
                        # Process each row based on the dataset name
                        processed_row = process_row(row, dataset_name)
                        if processed_row:  # Only add to documents if the row is valid
                            documents.append(processed_row)
                    except KeyError as e:
                        print(f"[WARNING] Missing field in row: {e}")
                    except Exception as e:
                        print(f"[ERROR] Error processing row: {e}")
                try:
                    if documents:  # Only insert if there are documents
                        collection.insert_many(documents)
                        print(f"[INFO] Successfully loaded {file_name} into {collection_name}")
                    else:
                        print(f"[INFO] No valid rows found in {file_name}")
                except Exception as e:
                    print(f"[ERROR] Failed to insert {file_name}: {e}")
            print(f"[INFO] Finished loading {file_name}")

            # Simulate MapReduce after loading data
            map_reduce_simulation(dataset_name, file_path)

    client.close()

def ingest():
    """Main function to ingest all non-structured datasets."""
    for dataset_name, info in DATASETS.items():
        load_csv_to_mongo(dataset_name, info["collection"])

if __name__ == "__main__":
    ingest()
