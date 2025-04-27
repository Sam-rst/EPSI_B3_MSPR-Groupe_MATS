import requests
import os
import json
import time

BASE_URL = os.getenv("API_URL", "http://api:8000")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin.admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")


def wait_for_api(max_retries=10, delay=3):
    print("Waiting for API to be ready...")
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("API is ready!")
                return
        except requests.exceptions.ConnectionError:
            pass

        print(f"Attempt {attempt + 1}/{max_retries} failed, retrying in {delay} sec...")
        time.sleep(delay)

    raise Exception("API not reachable after multiple attempts.")


def user_exists(username, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    r = requests.get(f"{BASE_URL}/users/{username}", headers=headers)
    return r.status_code == 200


def create_admin_user(username, password):
    payload = {
        "username": username,
        "password": password,
        "role_id": 1,
        "country_id": 1,
    }

    r = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(f"Create admin user: {r.status_code} - {r.text}")
    return r.status_code == 201


def connect():
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD},
    )
    if response.status_code == 200:
        print("Connected to API successfully!")
        return response.json()["access_token"]
    else:
        print(f"Failed to connect to API: {response.status_code} - {response.text}")
        return None


def import_data(endpoint, file_path, token=None):
    with open(file_path, "r", encoding="utf-8") as f:
        payload = json.load(f)

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.post(
        f"{BASE_URL}/{endpoint}/import", json=payload, headers=headers
    )
    print(f"Import {endpoint}: {response.status_code} - {response.text}")


if __name__ == "__main__":
    wait_for_api()

    token = connect()
    if token is None:
        print("Failed to connect to the API. Exiting...")
        exit(1)
    else:
        import_data("continents", "/data/continents.json", token)
        import_data("countries", "/data/countries.json", token)
        import_data("epidemics", "/data/epidemics.json", token)
        import_data("vaccines", "/data/vaccines.json", token)
        import_data("roles", "/data/roles.json", token)
