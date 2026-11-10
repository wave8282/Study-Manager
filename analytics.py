"""학습 기록 통계 계산 모듈."""
from datetime import date, timedelta
from collections import defaultdict

def subject_totals(records):
    totals = defaultdict(float)
    for item in records:
        totals[str(item.get("subject", "기타"))] += float(item.get("hours", 0))
    return dict(sorted(totals.items(), key=lambda pair: pair[1], reverse=True))

def period_summary(records, start, end):
    selected = []
    for item in records:
        try:
            day = date.fromisoformat(item.get("date", ""))
        except (TypeError, ValueError):
            continue
        if start <= day <= end:
            selected.append(item)
    return {"records": len(selected), "days": len({item["date"] for item in selected}),
            "hours": round(sum(float(item.get("hours", 0)) for item in selected), 2),
            "subjects": subject_totals(selected)}

def current_streak(records, today=None):
    today = today or date.today()
    days = set()
    for item in records:
        try:
            days.add(date.fromisoformat(item.get("date", "")))
        except (TypeError, ValueError):
            pass
    check = today if today in days else today - timedelta(days=1)
    streak = 0
    while check in days:
        streak += 1
        check -= timedelta(days=1)
    return streak, len(days)

def today_summary(records, today=None):
    today = today or date.today()
    rows = [item for item in records if item.get("date") == today.isoformat()]
    return {"count": len(rows), "hours": round(sum(float(x.get("hours", 0)) for x in rows), 2),
            "subjects": subject_totals(rows)}
