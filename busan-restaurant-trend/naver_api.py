import requests, os
from dotenv import load_dotenv
load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
DISTRICTS = ["부산 수영구", "부산 해운대구", "부산 남구"]
KEYWORDS = ["맛집", "음식점", "식당", "카페"]

def search_restaurants(district, keyword, display=5):
    url = "https://openapi.naver.com/v1/search/local.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {"query": f"{district} {keyword}", "display": display, "sort": "comment"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"[네이버 오류] {response.status_code}: {response.text}")
        return []
    results = []
    for item in response.json().get("items", []):
        name = item["title"].replace("<b>", "").replace("</b>", "")
        results.append({
            "name": name,
            "address": item.get("roadAddress") or item.get("address", ""),
            "district": district,
            "category": item.get("category", ""),
            "naver_link": item.get("link", "")
        })
    return results

def collect_all(display=5):
    all_results, seen = [], set()
    for district in DISTRICTS:
        for keyword in KEYWORDS:
            print(f"  🔍 네이버 검색 중: {district} {keyword}")
            for item in search_restaurants(district, keyword, display):
                key = (item["name"], item["address"])
                if key not in seen:
                    seen.add(key)
                    all_results.append(item)
    print(f"\n✅ 네이버에서 총 {len(all_results)}개 음식점 수집 완료\n")
    return all_results
