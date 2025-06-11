import logging

import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

ID = "6545e2f91cfa8764c963f550"
URL = f"https://cdn.amediatv.uz/api/season/v2/{ID}"
OUTPUT_FILE = "data.txt"


def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")
    return None


def save_data_to_file(data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"Season Name: {data['data']['name']['uz']}\n\n")
            text_data = []
            for item in data.get("seria", []):
                text_data.append(f"{item['name']['uz']}: {item['video']}")
            text_data.reverse()
            for line in text_data:
                file.write(line + "\n\n")
        logging.info("Data successfully saved to %s", file_path)
    except KeyError as e:
        logging.error(f"Missing expected key: {e}")
    except Exception as err:
        logging.error(f"Error while saving data: {err}")


def main():
    data = fetch_data(URL)
    if data:
        save_data_to_file(data, OUTPUT_FILE)


if __name__ == "__main__":
    main()
