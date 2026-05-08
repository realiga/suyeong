from database import get_review_history, get_all_restaurants

def analyze_trending(top_n=10):
    trending = []
    for name, address, district, category in get_all_restaurants():
        history = get_review_history(name, address)
        if len(history) < 2:
            if history:
                trending.append({"name": name, "address": address, "district": district,
                    "category": category, "current_reviews": history[-1][0],
                    "increase": None, "increase_rate": None, "recorded_at": history[-1][1]})
            continue
        first, latest = history[0][0], history[-1][0]
        increase = latest - first
        rate = round((increase / first) * 100, 1) if first > 0 else 0
        trending.append({"name": name, "address": address, "district": district,
            "category": category, "current_reviews": latest,
            "increase": increase, "increase_rate": rate, "recorded_at": history[-1][1]})
    trending.sort(key=lambda x: (x["increase"] or 0, x["current_reviews"]), reverse=True)
    return trending[:top_n]

def print_report(trending):
    print("\n" + "=" * 60)
    print("🍽️  부산 핫플 음식점 트렌드 리포트")
    print("     (수영구 · 해운대구 · 남구)")
    print("=" * 60)
    for i, r in enumerate(trending, 1):
        medal = "🥇" if i==1 else "🥈" if i==2 else "🥉" if i==3 else f"{i}위"
        print(f"\n{medal}  {r['name']}")
        print(f"   📍 {r['district']}  |  {r['category']}")
        print(f"   📊 현재 구글 리뷰: {r['current_reviews']:,}개", end="")
        if r["increase"] is not None:
            print(f"  📈  +{r['increase']}개 증가 ({r['increase_rate']}%↑)")
        else:
            print("  (첫 수집 데이터)")
        print(f"   🕐 최근 기록: {r['recorded_at'][:16]}")
    print("\n" + "=" * 60)
    print("💡 주기적으로 실행할수록 증가량 데이터가 쌓여요!")
    print("=" * 60 + "\n")
