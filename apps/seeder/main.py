import requests
import os
import json
import time

BASE_URL = os.getenv("API_URL", "http://api:8000")

def wait_for_api(max_retries=10, delay=3):
    print("Waiting for API to be ready...")
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health")  # ou /health si tu as
            if response.status_code == 200:
                print("API is ready!")
                return
        except requests.exceptions.ConnectionError:
            pass

        print(f"Attempt {attempt + 1}/{max_retries} failed, retrying in {delay} sec...")
        time.sleep(delay)

    raise Exception("API not reachable after multiple attempts.")

def import_data(endpoint, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        payload = json.load(f)

    response = requests.post(
        f"{BASE_URL}/{endpoint}/import",
        json=payload,
    )

    print(f"Import {endpoint}: {response.status_code} - {response.text}")


if __name__ == "__main__":
    wait_for_api()

    import_data("continents", "/data/continents.json")
    import_data("countries", "/data/countries.json")
    import_data("epidemics", "/data/epidemics.json")
    import_data("vaccines", "/data/vaccines.json")
