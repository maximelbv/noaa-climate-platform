import os
import requests
from concurrent.futures import ThreadPoolExecutor

# Configuration
DATASETS = {
    "gsod": {
        "url_pattern": "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{year}/",
        "years": range(2015, 2017),
    },
    "isd": {
        "url_pattern": "https://www.ncei.noaa.gov/data/integrated-surface-database/access/{year}/",
        "years": range(2015, 2017),
    },
    "storm_events": {
        "url_pattern": "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/",
        "years": range(2015, 2017),
    },
    "metar": {
        "url_pattern": "https://tgftp.nws.noaa.gov/data/observations/metar/stations/",
        "years": None,
    },
}
OUTPUT_DIR = "./data/raw"
MAX_DATASET_SIZE_GB = 10
BYTES_IN_GB = 1024 * 1024 * 1024

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def log_file_size(file_size):
    file_size_mb = file_size / (1024 * 1024)
    return f"{file_size_mb:.2f} MB" if file_size_mb < 1024 else f"{file_size_mb / 1024:.2f} GB"

def download_file(file_info):
    url, output_path, current_size, size_limit = file_info
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        file_size = int(response.headers.get('Content-Length', 0))
        if current_size + file_size > size_limit:
            print(f"⚠️ Skipping {url}: File would exceed dataset limit.")
            return file_size

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        print(f"✅ Downloaded: {url} ({log_file_size(file_size)})")
        return file_size
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading {url}: {e}")
        return 0

def download_dataset(dataset_name, dataset_info):
    dataset_dir = os.path.join(OUTPUT_DIR, dataset_name)
    ensure_directory_exists(dataset_dir)

    total_size_bytes = 0
    size_limit = MAX_DATASET_SIZE_GB * BYTES_IN_GB
    file_infos = []

    if dataset_info["years"]:
        for year in dataset_info["years"]:
            year_dir = os.path.join(dataset_dir, str(year))
            ensure_directory_exists(year_dir)

            url = dataset_info["url_pattern"].format(year=year)
            try:
                response = requests.get(url)
                response.raise_for_status()

                for line in response.text.splitlines():
                    if ".csv" in line or ".txt" in line:
                        file_name = line.split('href="')[1].split('"')[0]
                        file_url = url + file_name
                        output_path = os.path.join(year_dir, file_name)
                        file_infos.append((file_url, output_path, total_size_bytes, size_limit))
            except requests.exceptions.RequestException as e:
                print(f"❌ Error accessing {url}: {e}")
    else:
        try:
            response = requests.get(dataset_info["url_pattern"])
            response.raise_for_status()

            for line in response.text.splitlines():
                if ".csv" in line or ".txt" in line:
                    file_name = line.split('href="')[1].split('"')[0]
                    file_url = dataset_info["url_pattern"] + file_name
                    output_path = os.path.join(dataset_dir, file_name)
                    file_infos.append((file_url, output_path, total_size_bytes, size_limit))
        except requests.exceptions.RequestException as e:
            print(f"❌ Error accessing {dataset_info['url_pattern']}: {e}")

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(download_file, file_infos)

    total_size_bytes += sum(results)
    print(f"✅ Finished {dataset_name}: Total size downloaded = {log_file_size(total_size_bytes)}")

def main():
    ensure_directory_exists(OUTPUT_DIR)
    for dataset_name, dataset_info in DATASETS.items():
        download_dataset(dataset_name, dataset_info)

if __name__ == "__main__":
    main()
