import psycopg2

DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_DEFAULT_DB = "postgres"

CREATE_DB_SQL = """
DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'noaa') THEN
      CREATE DATABASE noaa;
   END IF;
END
$do$;
"""

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    station_id VARCHAR(50),
    date DATE,
    temperature FLOAT,
    precipitation FLOAT
);

CREATE TABLE IF NOT EXISTS metadata (
    id SERIAL PRIMARY KEY,
    description TEXT,
    source VARCHAR(100)
);
"""

def create_database():
    print("[INFO] Connecting to the default database...")
    conn = psycopg2.connect(
        dbname=DB_DEFAULT_DB,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            print("[INFO] Creating database 'noaa' if it does not exist...")
            cur.execute(CREATE_DB_SQL)
    finally:
        conn.close()

def create_tables():
    print("[INFO] Connecting to the 'noaa' database...")
    conn = psycopg2.connect(
        dbname="noaa",
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            print("[INFO] Creating tables in the 'noaa' database...")
            cur.execute(CREATE_TABLES_SQL)
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        create_database()
        create_tables()
        print("[INFO] Initialization completed successfully!")
    except Exception as e:
        print("[ERROR] An error occurred:", e)
