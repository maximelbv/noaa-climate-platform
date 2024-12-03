# NOAA Data Analysis Platform

The NOAA Data Analysis Platform is a project designed to analyze and visualize large-scale climatic datasets sourced from the National Oceanic and Atmospheric Administration (NOAA). The platform aims to:

- Simplify the retrieval, storage, and processing of structured data (e.g., GSOD) and unstructured data (e.g., Storm Events).
- Leverage advanced analytical tools to explore the datasets using modern technologies such as Hive, MongoDB, and ElasticSearch.
- Provide an intuitive web interface for users to query and visualize their data insights effectively.

This project was developed as part of an educational framework and focuses on integrating open-source solutions to handle big data challenges while optimizing data processing and visualization workflows.

## Docs

- [Brief of the project](/docs/brief.pdf)

## Features

- **Automated Data Retrieval**:

  - Python scripts to download structured (e.g., GSOD) and unstructured (e.g., Storm Events) datasets directly from NOAA sources.
  - Support for large datasets with robust error handling and progress tracking.

- **Data Storage and Organization**:

  - Hive: Store structured data with partitioning for efficient querying.
  - MongoDB: Manage unstructured data, including text-based storm reports.

- **Data Transformation and Processing**:

  - Data cleaning, normalization, and transformation using Python (Pandas).
  - Simulation of MapReduce workflows to process large datasets locally.

- **Advanced Search Capabilities**:

  - Integration with ElasticSearch to index and query both structured and unstructured data.
  - Creation of custom mappings to enhance search precision for climatic and geographical queries.

- **Web Application**:

  - Backend: FastAPI-powered API with JWT authentication for secure data access.
  - Frontend: Interactive React-based user interface for data visualization and querying.
  - Dynamic Graphs and Charts: Powered by D3.js for an engaging data visualization experience.

- **Security Features**:

  - JWT-based authentication for API endpoints.
    Configurable access permissions for Hive and MongoDB.
  - Theoretical implementation plan for Kerberos and SSL for data security.

- **Big Data Queries**:

  - HiveQL scripts for aggregations and large-scale data analysis (e.g., average, max, min temperatures).
  - MongoDB queries for filtering and keyword-based searches in storm reports.

- **Data Backup and Recovery**:

  - Automated data backup scripts simulating cloud storage.
  - Documented recovery procedures for restoring datasets.

- **Extensibility**:

  - Modular design with Dockerized components for easy deployment.
  - Scalable architecture, ready for cloud deployment and integration with tools like Apache Spark.

## Structure of the project

## Technologies used

#### **Data Processing and Storage**

- **Python**: Core language for data retrieval, transformation, and ingestion scripts.
- **Pandas**: Used for data cleaning, transformation, and simulating MapReduce workflows.
- **Hive (Standalone)**: Handles structured data storage and querying using HiveQL with partitioning for optimized performance.
- **MongoDB**: Stores unstructured data, such as textual storm reports, with a flexible schema for easy retrieval.

#### **Search and Indexing**

- **ElasticSearch**: Provides advanced search capabilities and enables querying across structured and unstructured datasets.

#### **Web Application**

- **FastAPI**: Backend framework for building RESTful APIs with high performance and JWT-based authentication.
- **React**: Frontend library for creating an interactive and responsive user interface.
- **D3.js**: JavaScript library for creating dynamic and interactive data visualizations.

#### **Containerization and Orchestration**

- **Docker**: Containerizes the various components of the platform for consistent and portable deployment.
- **Docker Compose**: Orchestrates the services, including Hive, MongoDB, ElasticSearch, and the web application.

#### **Infrastructure**

- **PostgreSQL**: Used as the Hive Metastore backend for managing metadata and schema definitions.
- **Linux (Ubuntu)**: Base image for most containers, ensuring compatibility and stability.

#### **Security**

- **JWT (JSON Web Tokens)**: Provides secure API authentication.
- **Theoretical Kerberos and SSL Configuration**: Plans for implementing robust access control and encryption.

#### **Development and Monitoring**

- **VS Code**: Primary IDE for development and debugging.
- **tqdm**: Provides progress bars for better feedback during dataset downloads.

## Prerequisites

Before setting up and running the NOAA Data Analysis Platform, ensure that the following prerequisites are met:

#### **System Requirements**

- **Operating System**: Linux, macOS, or Windows with Docker support.
- **Memory**: At least 8 GB of RAM recommended for running the Docker containers.
- **Storage**: At least 20 GB of free space for datasets and logs.

#### **Software Requirements**

- **Docker**: Installed and running. [Get Docker](https://www.docker.com/products/docker-desktop/)
- **Docker Compose**: Installed alongside Docker.
- **Python 3.9+**: Required for running the Python scripts.
- **Node.js**: Required if you need to modify the React frontend.

#### **Python Dependencies**

Ensure you have `pip` installed for managing Python packages. The required dependencies for the scripts are listed in:

- `scripts/requirements.txt` (for data processing and ingestion scripts).
- `web-app/backend/requirements.txt` (for the FastAPI backend).

#### **Optional Requirements**

- **Git**: To clone the repository and manage version control.
- **Postman**: Useful for testing API endpoints.
- **VS Code**: Recommended IDE for development.

#### **Dataset Sources**

Ensure you have access to the datasets from NOAA:

- Structured datasets (e.g., GSOD).
- Unstructured datasets (e.g., Storm Events).

## Installation

### Set up the Docker containers

```bash
# Make sure that you have the Docker daemon running
cd docker
docker-compose build
docker-compose up -d
```

### Download the data

```bash
# First, install the dependencies of the scripts
pip install -r scripts/requirements.txt

#Then, download the data
python3 scripts/download_data.py
```

### Set up & access the databases

#### **Postgres** :

```bash
# init the database
python3 scripts/init_postgres.py

# injest data to the database
python3 scripts/injest_postgres.py

# access the database
psql -h localhost -U postgres -d noaa
```

Ensure the database is created : `\l` <br />
Ensure the tables are created : `\dt`

You can verify the integrity of the data by making queries :

```sql
SELECT * FROM gsod_data LIMIT 10;
```

(you can quit the process with the `\q` command)

---

#### **Mongo** :

```bash
# init the database
python3 scripts/init_mongo.py

# injest data to the database
python3 scripts/injest_mongo.py

# access the database
mongosh -u admin -p password --authenticationDatabase admin
```

Ensure the database is created : `show dbs` <br />
Go to the noaa database:

```
use noaa
```

Ensure the collections are created : `show collections`

You can verify the integrity of the data by making queries :

```
db.storm_events.find().limit(10)
```

(you can quit the process with the `\q` command)

### Index data to Elastic Search

```
python3 scripts/elasticsearch/index_data.py
```

you can verify if the indexes are created by listing them:

```bash
curl -X GET "localhost:9200/_cat/indices?v"
```

or by getting the 10 first indexes:

```bash
curl -X GET "localhost:9200/mongo_storm_events_data/_search?pretty"
```

### Access the web-app

Client: http://localhost:3000

Server http://localhost:8000

Server Endpoints: http://localhost:8000/docs

## Querries List

> To analyse datas, you can make classic queries to each databases. I listed some usefull queries to analyse the data. You can also make more advanced and optimized queries with Elastic Search. I also listed a bunch of examples.

<details>
 <summary><strong>Structured data (Postgres)<strong></summary>
 
```sql
-- Get the maximum temperature for a specific station
SELECT "STATION", MAX("TEMP") AS max_temp
FROM "gsod_data"
WHERE "STATION" = 1001099999
GROUP BY "STATION";
```

```sql
-- Get the minimum temperature for a specific station
SELECT "STATION", MIN("TEMP") AS min_temp
FROM "gsod_data"
WHERE "STATION" = 1001099999
GROUP BY "STATION";
```

```sql
-- Get the average temperature for a specific station
SELECT "STATION", AVG("TEMP") AS avg_temp
FROM "gsod_data"
WHERE "STATION" = 1001099999
GROUP BY "STATION";
```

```sql
-- Get the total precipitation for a specific station
SELECT "STATION", SUM("PRCP") AS total_precipitation
FROM "gsod_data"
WHERE "STATION" = 1001099999
GROUP BY "STATION";
```

```sql
-- Get the average temperature by year
SELECT EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD')) AS year,
       AVG("TEMP") AS avg_temp
FROM "gsod_data"
GROUP BY year
ORDER BY year;
```

```sql
-- Get the average precipitation by year
SELECT EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD')) AS year,
       AVG("PRCP") AS avg_precipitation
FROM "gsod_data"
GROUP BY year
ORDER BY year;
```

```sql
-- Identify trends in average temperature over multiple years
SELECT EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD')) AS year,
       AVG("TEMP") AS avg_temp
FROM "gsod_data"
GROUP BY year
ORDER BY year;
```

```sql
-- Get the average temperature for a specific station over time
SELECT EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD')) AS year,
       AVG("TEMP") AS avg_temp
FROM "gsod_data"
WHERE "STATION" = 1001099999
GROUP BY year
ORDER BY year;
```

```sql
-- Get the maximum temperature for a specific station over time
SELECT EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD')) AS year,
       MAX("TEMP") AS max_temp
FROM "gsod_data"
WHERE "STATION" = 1001099999
GROUP BY year
ORDER BY year;
```

```sql
-- Get the minimum temperature for a specific station over time
SELECT EXTRACT(YEAR FROM TO_DATE("DATE", 'YYYY-MM-DD')) AS year,
       MIN("TEMP") AS min_temp
FROM "gsod_data"
WHERE "STATION" = 1001099999
GROUP BY year
ORDER BY year;
```

```sql
-- Get the top 10 stations with the highest maximum temperature
SELECT "STATION", MAX("TEMP") AS max_temp
FROM "gsod_data"
GROUP BY "STATION"
ORDER BY max_temp DESC
LIMIT 10;
```

```sql
-- Get the top 10 states with the highest total precipitation
SELECT "STATE", SUM("PRCP") AS total_precipitation
FROM "gsod_data"
GROUP BY "STATE"
ORDER BY total_precipitation DESC
LIMIT 10;
```

</details>

<details>
  <summary><strong>Unstructured data (Mongo)</strong></summary>

```bash
# Count events
db.storm_events.countDocuments()
```

```bash
# Find all events of a specific type (e.g., Excessive Heat)
db.storm_events.countDocuments({ EVENT_TYPE: "Excessive Heat" })
```

```bash
# Find all events in a specific year (e.g., 2019)
db.storm_events.find({ YEAR: "2019" })
```

```bash
# Find events by state (e.g., Arizona)
db.storm_events.find({ STATE: "ARIZONA" })
```

```bash
# Get all distinct event types in the collection
db.storm_events.distinct("EVENT_TYPE")
```

```bash
# Group by event type and count occurrences
db.storm_events.aggregate([
    {
        $group: {
            _id: "$EVENT_TYPE",
            count: { $sum: 1 }
        }
    },
    {
        $sort: { count: -1 }
    }
])
```

```bash
# Get events that occurred within a specific time range (e.g., August 30, 2019, to August 31, 2019)
db.storm_events.find({
    BEGIN_DATE_TIME: { $gte: "30-AUG-19 00:00:00", $lte: "31-AUG-19 23:59:59" }
})
```

```bash
# Find events with injuries or deaths
db.storm_events.find({
    $or: [
        { INJURIES_DIRECT: { $gt: 0 } },
        { INJURIES_INDIRECT: { $gt: 0 } },
        { DEATHS_DIRECT: { $gt: 0 } },
        { DEATHS_INDIRECT: { $gt: 0 } }
    ]
})
```

```bash
# Aggregate events by location (e.g., by CZ_NAME or STATE)
db.storm_events.aggregate([
    {
        $group: {
            _id: "$CZ_NAME",
            count: { $sum: 1 }
        }
    },
    {
        $sort: { count: -1 }
    }
])
```

```bash
# Find events that mention 'storm' in their narratives
db.storm_events.find({
    $or: [
        { "EPISODE_NARRATIVE": { $regex: "storm", $options: "i" } }, # Case-insensitive search
        { "EVENT_NARRATIVE": { $regex: "storm", $options: "i" } }
    ]
})
```

```bash
# Find storm events that mention either 'storm' or 'heat' in their narratives
db.storm_events.find({
    $or: [
        { "EPISODE_NARRATIVE": { $regex: "storm|heat", $options: "i" } },
        { "EVENT_NARRATIVE": { $regex: "storm|heat", $options: "i" } }
    ]
})
```

```bash
# Find storm events that mention both 'storm' and 'damage' in the narratives
db.storm_events.find({
    $and: [
        { "EPISODE_NARRATIVE": { $regex: "storm", $options: "i" } },
        { "EVENT_NARRATIVE": { $regex: "damage", $options: "i" } }
    ]
})
```

```bash
# Count the number of events that mention 'storm' in the narrative
db.storm_events.countDocuments({
    $or: [
        { "EPISODE_NARRATIVE": { $regex: "storm", $options: "i" } },
        { "EVENT_NARRATIVE": { $regex: "storm", $options: "i" } }
    ]
})
```

#### Large volumes specific queries

```bash
# Paginate through the events collection by skipping the first 1000 records and limiting to 100 records per page
db.storm_events.aggregate([
    { $skip: 1000 },
    { $limit: 100 }
])
```

```bash
# Find the first 100 events where property damage is greater than 0
db.storm_events.find({ DAMAGE_PROPERTY: { $ne: "0.00K" } }).limit(100)

```

```bash
# Get events with the highest property damage (top 10)
db.storm_events.aggregate([
    {
        $match: { DAMAGE_PROPERTY: { $ne: "0.00K" } }
    },
    {
        $sort: { DAMAGE_PROPERTY: -1 }
    },
    {
        $limit: 10
    }
])
```

```bash
# Create an index on 'EVENT_TYPE' for faster queries
db.storm_events.createIndex({ "EVENT_TYPE": 1 })

# Now we can run an optimized query to fetch events by type quickly
db.storm_events.find({ EVENT_TYPE: "Excessive Heat" })
```

```bash
# Use an index on BEGIN_DATE_TIME for fast date filtering
db.storm_events.createIndex({ "BEGIN_DATE_TIME": 1 })

# Find events that occurred between specific dates (e.g., 2019-08-01 to 2019-08-31)
db.storm_events.find({
    BEGIN_DATE_TIME: { $gte: "01-AUG-19", $lte: "31-AUG-19" }
})

```

</details>

<details>
 <summary><strong>Querying with Elastic Search (unstructured data only for the moment)<strong></summary>

```bash
# Get all events of type "Thunderstorm Wind"
curl -X GET "localhost:9200/mongo_storm_events_data/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "EVENT_TYPE": "Thunderstorm Wind"
    }
  }
}
'
```

```bash
# Get events from a specific state (e.g., "NEW YORK")
curl -X GET "localhost:9200/mongo_storm_events_data/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {
      "STATE.keyword": "NEW YORK"
    }
  }
}
'
```

```bash
# Aggregate the total number of events by event type
curl -X GET "localhost:9200/mongo_storm_events_data/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "events_by_type": {
      "terms": {
        "field": "EVENT_TYPE.keyword",
        "size": 10
      }
    }
  }
}
'
```

```bash
# Get the most recent event in a specific state
curl -X GET "localhost:9200/mongo_storm_events_data/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "term": {
      "STATE.keyword": "NEW YORK"
    }
  },
  "sort": [
    {
      "BEGIN_DATE_TIME": {
        "order": "desc"
      }
    }
  ],
  "size": 1
}
'
```

```bash
# Find events with significant damage (e.g., `DAMAGE_PROPERTY` > 1000)
curl -X GET "localhost:9200/mongo_storm_events_data/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "DAMAGE_PROPERTY": {
        "gte": 1000
      }
    }
  }
}
'
```

```bash
# Search for events that occurred in a specific geographic region
curl -X GET "localhost:9200/mongo_storm_events_data/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "BEGIN_LAT": {
              "gte": 40,
              "lte": 41
            }
          }
        },
        {
          "range": {
            "BEGIN_LON": {
              "gte": -75,
              "lte": -74
            }
          }
        }
      ]
    }
  }
}
'

```

</details>
