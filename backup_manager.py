"""JSON 데이터 백업 및 안전한 복원."""
import json
import shutil
from datetime import datetime
from pathlib import Path

def create_backup(filenames, backup_dir="backups"):
    folder = Path(backup_dir)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    created = []
    for name in filenames:
        source = Path(name)
        if source.is_file():
            target = folder / f"{stamp}_{source.name}"
            shutil.copy2(source, target)
            created.append(target)
    return created

def restore_backup(backup_file, target_file):
    source, target = Path(backup_file), Path(target_file)
    if not source.is_file():
        raise FileNotFoundError(f"백업 파일을 찾을 수 없습니다: {source}")
    with source.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if target.name == "study_data.json" and not (isinstance(data, list) and all(isinstance(x, dict) for x in data)):
        raise ValueError("공부 기록 백업 형식이 올바르지 않습니다.")
    if target.name == "study_settings.json" and not isinstance(data, dict):
        raise ValueError("설정 백업 형식이 올바르지 않습니다.")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target
