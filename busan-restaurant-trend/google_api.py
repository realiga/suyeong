import requests, os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_review_info(name, address):
    """Places API (New) - Text Search로 리뷰 정보 조회"""
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.rating,places.userRatingCount"
    }
    body = {
        "textQuery": f"{name} {address}",
        "languageCode": "ko"
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        print(f"    [구글 오류] {response.status_code}: {response.text}")
        return None

    places = response.json().get("places", [])
    if not places:
        return None

    place = places[0]
    return {
        "rating": place.get("rating", 0),
        "review_count": place.get("userRatingCount", 0)
    }
