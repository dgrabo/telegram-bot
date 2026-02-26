import requests
import json
import os
from dotenv import load_dotenv
import logging

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

logger = logging.getLogger(__name__)

def search_restaurants(lat, lng, radius):
    url = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.location"
    }
    body = {
        "includedTypes": ["restaurant"],
        "maxResultCount": 5,
        "locationRestriction":
        {
            "circle": {
                "center":{
                    "latitude": lat, "longitude": lng
                },
                "radius": radius
            }
        }
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    logger.info(json.dumps(data, indent=2, ensure_ascii=False))
    return data