"""입력값 검증 함수."""
import math
from datetime import date

def parse_hours(value):
    try:
        hours = float(value)
    except (TypeError, ValueError):
        raise ValueError("공부 시간은 숫자로 입력해야 합니다.")
    if not math.isfinite(hours) or hours <= 0 or hours > 24:
        raise ValueError("공부 시간은 0보다 크고 24 이하여야 합니다.")
    return round(hours, 2)

def parse_date(value):
    try:
        return date.fromisoformat(str(value)).isoformat()
    except (TypeError, ValueError):
        raise ValueError("날짜는 YYYY-MM-DD 형식으로 입력해야 합니다.")

def required_text(value, label="항목"):
    text = str(value).strip()
    if not text:
        raise ValueError(f"{label}을(를) 입력해 주세요.")
    return text
