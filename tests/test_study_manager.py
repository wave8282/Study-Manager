"""핵심 로직 자동 테스트: python -m unittest discover -s tests"""
import unittest
from datetime import date
from analytics import subject_totals, current_streak, today_summary
from study_service import StudyService
from validators import parse_hours, parse_date

class StudyManagerTests(unittest.TestCase):
    def setUp(self):
        self.records = []
        self.service = StudyService(self.records, lambda data: None)

    def test_add_record(self):
        row = self.service.add("한국사", "2.5", "고대사", "2026-11-10")
        self.assertEqual(row["hours"], 2.5)
        self.assertEqual(len(self.records), 1)

    def test_update_record(self):
        self.service.add("한국사", 1)
        self.service.update(0, subject="영어", hours=2)
        self.assertEqual(self.records[0]["subject"], "영어")
        self.assertEqual(self.records[0]["hours"], 2)

    def test_delete_record(self):
        self.service.add("한국사", 1)
        self.service.delete(0)
        self.assertEqual(self.records, [])

    def test_search_record(self):
        self.service.add("한국사", 1, "고대 국가")
        self.assertEqual(len(self.service.search("고대")), 1)

    def test_invalid_hours(self):
        with self.assertRaises(ValueError):
            parse_hours(0)

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            parse_date("2026/11/10")

    def test_subject_totals(self):
        self.assertEqual(subject_totals([{"subject":"영어","hours":2}])["영어"], 2)

    def test_today_summary(self):
        today = date(2026, 11, 10)
        self.assertEqual(today_summary([{"date":"2026-11-10","subject":"영어","hours":2}], today)["hours"], 2)

    def test_streak(self):
        today = date(2026, 11, 10)
        rows = [{"date":"2026-11-09"}, {"date":"2026-11-10"}]
        self.assertEqual(current_streak(rows, today)[0], 2)

if __name__ == "__main__":
    unittest.main()
