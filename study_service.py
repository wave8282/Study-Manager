"""공부 기록의 추가·수정·삭제·검색을 담당합니다."""
from datetime import date
from validators import parse_hours, parse_date, required_text

class StudyService:
    def __init__(self, records, save_callback):
        self.records = records
        self.save_callback = save_callback

    def add(self, subject, hours, memo="", study_date=None):
        item = {"date": parse_date(study_date or date.today().isoformat()),
                "subject": required_text(subject, "과목명"),
                "hours": parse_hours(hours), "memo": str(memo).strip()}
        self.records.append(item)
        self.save_callback(self.records)
        return item

    def update(self, index, **changes):
        if not 0 <= index < len(self.records):
            raise IndexError("기록 번호가 올바르지 않습니다.")
        item = self.records[index]
        if changes.get("subject") is not None:
            item["subject"] = required_text(changes["subject"], "과목명")
        if changes.get("hours") is not None:
            item["hours"] = parse_hours(changes["hours"])
        if changes.get("date") is not None:
            item["date"] = parse_date(changes["date"])
        if changes.get("memo") is not None:
            item["memo"] = str(changes["memo"]).strip()
        self.save_callback(self.records)
        return item

    def delete(self, index):
        if not 0 <= index < len(self.records):
            raise IndexError("기록 번호가 올바르지 않습니다.")
        item = self.records.pop(index)
        self.save_callback(self.records)
        return item

    def search(self, keyword):
        keyword = str(keyword).strip().casefold()
        if not keyword:
            return []
        return [(i, row) for i, row in enumerate(self.records)
                if keyword in " ".join(str(row.get(k, "")) for k in ("date", "subject", "memo")).casefold()]
