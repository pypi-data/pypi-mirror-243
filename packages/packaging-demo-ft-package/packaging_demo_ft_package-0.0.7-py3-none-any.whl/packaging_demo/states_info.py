from pathlib import Path
import json
from typing import List

# the absolute path of this file
THIS_DIR = Path(__file__).parent

# relative path to the datafile
CITIES_JSON_PATH = THIS_DIR / "./cities.json"
print(CITIES_JSON_PATH)


def is_city_capitol_of_state(city_name: str, state: str) -> bool:
    cities_json_contents = CITIES_JSON_PATH.read_text()
    cities: List[dict] = json.loads(cities_json_contents)
    matching_cities: List[dict] = [c for c in cities if c["city"] == city_name]
    if len(matching_cities) == 0:
        return False
    matched_city = matching_cities[0]
    return matched_city["state"] == state


if __name__ == "__main__":
    print(is_city_capitol_of_state(city_name="Montgomery", state="Alabama"))
