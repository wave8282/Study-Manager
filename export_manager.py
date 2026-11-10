"""학습 기록을 CSV로 내보냅니다."""
import csv
from pathlib import Path

def export_records(records, filename="study_records.csv"):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["날짜", "과목", "공부 시간", "공부 내용"])
        for item in records:
            writer.writerow([item.get("date", ""), item.get("subject", ""),
                             item.get("hours", 0), item.get("memo", "")])
    return path
