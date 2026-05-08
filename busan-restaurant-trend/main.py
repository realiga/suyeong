import time
from database import init_db, save_restaurant, save_review_snapshot
from naver_api import collect_all
from google_api import get_review_info
from analyzer import analyze_trending, print_report

def main():
    print("\n🚀 부산 음식점 트렌드 수집 시작!\n")
    init_db()
    print("📡 [1단계] 네이버 검색 API로 음식점 수집 중...")
    restaurants = collect_all(display=5)
    print("📡 [2단계] 구글 Places API로 리뷰 정보 수집 중...")
    success_count = 0
    for i, r in enumerate(restaurants):
        print(f"  ({i+1}/{len(restaurants)}) {r['name']} 조회 중...")
        save_restaurant(r["name"], r["address"], r["district"], r["category"], r["naver_link"])
        review_info = get_review_info(r["name"], r["address"])
        if review_info:
            save_review_snapshot(r["name"], r["address"], review_info["rating"], review_info["review_count"])
            success_count += 1
        else:
            print(f"    ⚠️  구글에서 '{r['name']}' 정보를 찾지 못했습니다.")
        time.sleep(0.3)
    print(f"\n✅ 구글 리뷰 수집 완료: {success_count}/{len(restaurants)}개\n")
    print("📊 [3단계] 트렌딩 분석 중...")
    print_report(analyze_trending(top_n=10))

if __name__ == "__main__":
    main()
