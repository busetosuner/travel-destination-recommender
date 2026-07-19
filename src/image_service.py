import os
from functools import lru_cache

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PEXELS_API_KEY")


IMAGE_SEARCH_OVERRIDES = {
    "Crete": "Crete beach Greece",
    "Sardinia": "Sardinia beach Italy",
    "Puglia": "Puglia Italy coast",
    "Taormina": "Taormina Sicily Italy",
    "Tuscany": "Tuscany Italy landscape",
    "Barcelona": "Barcelona Spain architecture",
    "Zermatt": "Zermatt Matterhorn Switzerland",
    "Hallstatt": "Hallstatt Austria lake",
    "Dubrovnik": "Dubrovnik old town Croatia",
    "Kotor": "Kotor Montenegro bay",
    "Mostar": "Mostar Bosnia old bridge",
    "Istanbul": "Istanbul Turkey skyline",
}


@lru_cache(maxsize=200)
def get_city_image(city: str, country: str):
    if not API_KEY:
        return None

    headers = {
        "Authorization": API_KEY
    }

    query = IMAGE_SEARCH_OVERRIDES.get(
        city,
        f"{city} {country} travel destination"
    )

    response = requests.get(
        "https://api.pexels.com/v1/search",
        headers=headers,
        params={
            "query": query,
            "per_page": 1,
            "orientation": "landscape",
        },
        timeout=10
    )

    if response.status_code != 200:
        return None

    data = response.json()

    if not data.get("photos"):
        return None

    return data["photos"][0]["src"]["landscape"]