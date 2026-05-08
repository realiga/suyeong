from database import get_review_history, get_all_restaurants

def analyze_trending(top_n=10):
    """리뷰 증가량 기준으로 트렌딩 음식점 분석"""
    restaurants = get_all_restaurants()
    trending = []

    for name, address, district, category in restaurants:
        history = get_review_history(name, address)

        if len(history) < 2:
            # 기록이 1개뿐이면 현재 리뷰수만 표시
            if history:
                trending.append({
                    "name": name,
                    "address": address,
                    "district": district,
                    "category": category,
                    "current_reviews": history[-1][0],
                    "increase": None,
                    "increase_rate": None,
                    "recorded_at": history[-1][1]
                })
            continue

        first_count = history[0][0]   # 첫 기록
        latest_count = history[-1][0]  # 최신 기록
        increase = latest_count - first_count

        if first_count > 0:
            increase_rate = round((increase / first_count) * 100, 1)
        else:
            increase_rate = 0

        trending.append({
            "name": name,
            "address": address,
            "district": district,
            "category": category,
            "current_reviews": latest_count,
            "increase": increase,
            "increase_rate": increase_rate,
            "recorded_at": history[-1][1]
        })

    # 리뷰 증가량 기준 정렬 (증가량 없으면 현재 리뷰수 기준)
    trending.sort(
        key=lambda x: (x["increase"] or 0, x["current_reviews"]),
        reverse=True
    )

    return trending[:top_n]

def print_report(trending):
    """결과 출력"""
    print("\n" + "=" * 60)
    print("🍽️  부산 핫플 음식점 트렌드 리포트")
    print("     (수영구 · 해운대구 · 남구)")
    print("=" * 60)

    for i, r in enumerate(trending, 1):
        print(f"\n{'🥇' if i==1 else '🥈' if i==2 else '🥉' if i==3 else f'{i}위'}  {r['name']}")
        print(f"   📍 {r['district']}  |  {r['category']}")
        print(f"   📊 현재 구글 리뷰: {r['current_reviews']:,}개", end="")

        if r["increase"] is not None:
            arrow = "📈" if r["increase"] > 0 else "➡️"
            print(f"  {arrow}  +{r['increase']}개 증가 ({r['increase_rate']}%↑)")
        else:
            print("  (첫 수집 데이터)")

        print(f"   🕐 최근 기록: {r['recorded_at'][:16]}")

    print("\n" + "=" * 60)
    print(f"💡 Tip: 프로그램을 주기적으로 실행할수록 증가량 데이터가 쌓여요!")
    print("=" * 60 + "\n")