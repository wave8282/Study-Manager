"""JSON 파일 저장과 로드 기능을 담당합니다."""
import json
from pathlib import Path

class JSONStorage:
    def __init__(self, filename, default):
        self.path = Path(filename)
        self.default = default

    def load(self):
        if not self.path.exists():
            return self.default.copy() if isinstance(self.default, (dict, list)) else self.default
        try:
            with self.path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print(f"[경고] {self.path} 파일을 읽지 못했습니다. 기본값을 사용합니다.")
            return self.default.copy() if isinstance(self.default, (dict, list)) else self.default

    def save(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        temp_path.replace(self.path)
