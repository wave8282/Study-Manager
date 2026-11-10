"""하루 및 과목별 학습 목표 관리."""
from storage import JSONStorage
from validators import parse_hours, required_text

class GoalManager:
    def __init__(self, filename="study_settings.json"):
        self.store = JSONStorage(filename, {"daily_goal": 3.0, "subject_goals": {}})
        self.settings = self.store.load()
        if not isinstance(self.settings, dict):
            self.settings = {}
        self.settings.setdefault("daily_goal", 3.0)
        self.settings.setdefault("subject_goals", {})

    def set_daily_goal(self, hours):
        self.settings["daily_goal"] = parse_hours(hours)
        self.store.save(self.settings)

    def set_subject_goal(self, subject, hours):
        subject = required_text(subject, "과목명")
        self.settings["subject_goals"][subject] = parse_hours(hours)
        self.store.save(self.settings)

    def daily_status(self, studied):
        goal = float(self.settings["daily_goal"])
        return {"goal": goal, "studied": studied, "remaining": max(0, goal-studied),
                "percent": min(100, round(studied/goal*100, 1))}

    def subject_status(self, totals):
        result = {}
        for subject, goal in self.settings["subject_goals"].items():
            studied = float(totals.get(subject, 0))
            result[subject] = {"goal": float(goal), "studied": studied,
                "percent": round(studied/float(goal)*100, 1),
                "remaining": max(0, float(goal)-studied)}
        return result
