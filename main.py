import csv
import json
import math
import os
import shutil
from datetime import date, datetime, timedelta

FILE_NAME = "study_data.json"
SETTINGS_FILE = "study_settings.json"


def load_json(filename, default):
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print(f"{filename} 파일을 읽을 수 없습니다. 기본값을 사용합니다.")
        return default


def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_data():
    data = load_json(FILE_NAME, [])
    if not isinstance(data, list):
        print("공부 기록 형식이 올바르지 않습니다. 빈 목록으로 시작합니다.")
        return []
    return [item for item in data if isinstance(item, dict)]


def load_settings():
    settings = load_json(SETTINGS_FILE, {})
    if not isinstance(settings, dict):
        settings = {}
    settings.setdefault("daily_goal", 3.0)
    settings.setdefault("subject_goals", {})
    return settings


def save_data(data):
    save_json(FILE_NAME, data)


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


def input_hours(prompt):
    while True:
        try:
            value = float(input(prompt))
            if not math.isfinite(value) or value <= 0:
                print("0보다 큰 숫자를 입력해 주세요.")
                continue
            return round(value, 2)
        except ValueError:
            print("숫자로 입력해 주세요.")


def valid_date(value):
    try:
        return date.fromisoformat(value).isoformat()
    except (ValueError, TypeError):
        return None


def add_study(data):
    print("\n[ 공부 기록 추가 ]")
    subject = input("과목명: ").strip()
    if not subject:
        print("과목명을 입력해 주세요.")
        return
    hours = input_hours("공부 시간(시간): ")
    memo = input("공부 내용: ").strip()
    data.append({
        "date": date.today().isoformat(),
        "subject": subject,
        "hours": hours,
        "memo": memo
    })
    save_data(data)
    print("공부 기록이 저장되었습니다!")


def show_study(data):
    if not data:
        print("등록된 공부 기록이 없습니다.")
        return
    print("\n[ 공부 기록 목록 ]")
    for index, record in enumerate(data, 1):
        print(f"\n{index}. 날짜: {record.get('date', '정보 없음')}")
        print(f"   과목: {record.get('subject', '정보 없음')}")
        print(f"   시간: {record.get('hours', 0)}시간")
        print(f"   내용: {record.get('memo', '')}")


def show_total(data):
    total = sum(float(record.get("hours", 0)) for record in data)
    print(f"\n누적 공부 시간: {total:.1f}시간")


def show_subject_stats(data):
    stats = {}
    for record in data:
        subject = record.get("subject", "기타")
        stats[subject] = stats.get(subject, 0) + float(record.get("hours", 0))
    if not stats:
        print("등록된 공부 기록이 없습니다.")
        return
    print("\n[ 과목별 공부 시간 ]")
    for subject, hours in sorted(stats.items(), key=lambda item: item[1], reverse=True):
        print(f"{subject}: {hours:.1f}시간")


def delete_study(data):
    if not data:
        print("삭제할 기록이 없습니다.")
        return
    show_study(data)
    try:
        number = int(input("\n삭제할 기록 번호: "))
        if not 1 <= number <= len(data):
            print("올바른 번호를 입력해 주세요.")
            return
    except ValueError:
        print("숫자로 입력해 주세요.")
        return
    deleted = data.pop(number - 1)
    save_data(data)
    print(f"{deleted.get('subject', '공부')} 기록이 삭제되었습니다.")


def edit_study(data):
    if not data:
        print("수정할 기록이 없습니다.")
        return
    show_study(data)
    try:
        number = int(input("\n수정할 기록 번호: "))
        if not 1 <= number <= len(data):
            print("올바른 번호를 입력해 주세요.")
            return
    except ValueError:
        print("숫자로 입력해 주세요.")
        return

    record = data[number - 1]
    print("변경하지 않을 항목은 Enter를 누르세요.")
    subject = input(f"과목명 [{record.get('subject', '')}]: ").strip()
    if subject:
        record["subject"] = subject

    while True:
        value = input(f"공부 시간 [{record.get('hours', 0)}]: ").strip()
        if not value:
            break
        try:
            hours = float(value)
            if not math.isfinite(hours) or hours <= 0:
                print("0보다 큰 숫자를 입력해 주세요.")
                continue
            record["hours"] = round(hours, 2)
            break
        except ValueError:
            print("숫자로 입력해 주세요.")

    memo = input(f"공부 내용 [{record.get('memo', '')}]: ").strip()
    if memo:
        record["memo"] = memo

    current = record.get("date", date.today().isoformat())
    new_date = input(f"공부 날짜 [{current}] (YYYY-MM-DD): ").strip()
    if new_date:
        parsed = valid_date(new_date)
        if parsed:
            record["date"] = parsed
        else:
            print("날짜 형식이 올바르지 않아 기존 날짜를 유지합니다.")

    save_data(data)
    print("공부 기록이 수정되었습니다.")


def search_study(data):
    keyword = input("\n검색어(과목·날짜·메모): ").strip().lower()
    if not keyword:
        print("검색어를 입력해 주세요.")
        return
    results = [
        item for item in data
        if keyword in str(item.get("subject", "")).lower()
        or keyword in str(item.get("date", "")).lower()
        or keyword in str(item.get("memo", "")).lower()
    ]
    if not results:
        print("검색 결과가 없습니다.")
        return
    print(f"\n[ 검색 결과 {len(results)}건 ]")
    for index, item in enumerate(results, 1):
        print(f"{index}. {item.get('date')} | {item.get('subject')} | {item.get('hours')}시간 | {item.get('memo', '')}")


def period_records(data, start, end):
    results = []
    for item in data:
        record_date = valid_date(item.get("date"))
        if record_date and start <= date.fromisoformat(record_date) <= end:
            results.append(item)
    return results


def show_period_stats(data):
    print("\n1. 이번 주  2. 이번 달")
    choice = input("선택: ").strip()
    today = date.today()
    if choice == "1":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        title = f"{start} ~ {end}"
    elif choice == "2":
        start = today.replace(day=1)
        end = today
        title = today.strftime("%Y년 %m월")
    else:
        print("올바른 메뉴를 선택해 주세요.")
        return

    records = period_records(data, start, end)
    total = sum(float(item.get("hours", 0)) for item in records)
    days = len({item.get("date") for item in records})
    print(f"\n[ {title} ]")
    print(f"기록 {len(records)}건 | 공부한 날짜 {days}일 | 총 {total:.1f}시간")
    stats = {}
    for item in records:
        subject = item.get("subject", "기타")
        stats[subject] = stats.get(subject, 0) + float(item.get("hours", 0))
    for subject, hours in sorted(stats.items(), key=lambda pair: pair[1], reverse=True):
        print(f"- {subject}: {hours:.1f}시간")


def set_daily_goal(settings):
    print(f"\n현재 하루 목표: {settings.get('daily_goal', 3.0)}시간")
    try:
        goal = float(input("새로운 하루 목표 시간: "))
        if not math.isfinite(goal) or goal <= 0:
            print("0보다 큰 숫자를 입력해 주세요.")
            return
        settings["daily_goal"] = round(goal, 2)
        save_settings(settings)
        print("하루 목표를 저장했습니다.")
    except ValueError:
        print("숫자로 입력해 주세요.")


def show_daily_goal(data, settings):
    today = date.today().isoformat()
    total = sum(float(item.get("hours", 0)) for item in data if item.get("date") == today)
    goal = float(settings.get("daily_goal", 3.0))
    print(f"\n오늘 공부: {total:.1f}시간 / 목표: {goal:.1f}시간")
    if total >= goal:
        print(f"목표 달성! {total - goal:.1f}시간 초과했습니다.")
    else:
        print(f"목표까지 {goal - total:.1f}시간 남았습니다.")


def show_streak(data):
    study_days = {date.fromisoformat(item["date"]) for item in data if valid_date(item.get("date"))}
    if not study_days:
        print("아직 공부 기록이 없습니다.")
        return
    today = date.today()
    check = today if today in study_days else today - timedelta(days=1)
    streak = 0
    while check in study_days:
        streak += 1
        check -= timedelta(days=1)
    print(f"\n현재 연속 학습일: {streak}일")
    print(f"누적 학습일: {len(study_days)}일")


def export_csv(data):
    if not data:
        print("내보낼 공부 기록이 없습니다.")
        return
    filename = f"study_records_{date.today().isoformat()}.csv"
    try:
        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["날짜", "과목", "공부 시간", "공부 내용"])
            for item in data:
                writer.writerow([item.get("date", ""), item.get("subject", ""), item.get("hours", 0), item.get("memo", "")])
        print(f"CSV 저장 완료: {filename}")
    except OSError as error:
        print(f"CSV 저장 실패: {error}")


def show_today_summary(data):
    today = date.today().isoformat()
    records = [item for item in data if item.get("date") == today]
    total = sum(float(item.get("hours", 0)) for item in records)
    subjects = {}
    for item in records:
        subject = item.get("subject", "기타")
        subjects[subject] = subjects.get(subject, 0) + float(item.get("hours", 0))

    print("\n[ 오늘의 학습 요약 ]")
    print(f"기록 수: {len(records)}건")
    print(f"공부한 과목: {len(subjects)}개")
    print(f"총 공부 시간: {total:.1f}시간")
    if subjects:
        best = max(subjects, key=subjects.get)
        print(f"가장 많이 공부한 과목: {best} ({subjects[best]:.1f}시간)")
        for subject, hours in sorted(subjects.items(), key=lambda pair: pair[1], reverse=True):
            print(f"- {subject}: {hours:.1f}시간")
    else:
        print("오늘 등록된 공부 기록이 없습니다.")


def set_subject_goal(settings):
    subject = input("\n목표를 설정할 과목명: ").strip()
    if not subject:
        print("과목명을 입력해 주세요.")
        return
    try:
        goal = float(input(f"{subject} 주간 목표 시간: "))
        if not math.isfinite(goal) or goal <= 0:
            print("0보다 큰 숫자를 입력해 주세요.")
            return
    except ValueError:
        print("숫자로 입력해 주세요.")
        return
    settings.setdefault("subject_goals", {})[subject] = round(goal, 2)
    save_settings(settings)
    print(f"{subject} 주간 목표를 {goal:.1f}시간으로 설정했습니다.")


def show_subject_goals(data, settings):
    goals = settings.get("subject_goals", {})
    if not goals:
        print("설정된 과목별 주간 목표가 없습니다.")
        return
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    records = period_records(data, start, end)
    print(f"\n[ 과목별 주간 목표: {start} ~ {end} ]")
    for subject, goal in goals.items():
        studied = sum(float(item.get("hours", 0)) for item in records if item.get("subject") == subject)
        percent = studied / float(goal) * 100 if float(goal) else 0
        print(f"{subject}: {studied:.1f}/{float(goal):.1f}시간 ({percent:.0f}%)")
        if studied >= float(goal):
            print("  목표 달성!")
        else:
            print(f"  남은 시간: {float(goal) - studied:.1f}시간")


def backup_data():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    files_to_backup = [FILE_NAME, SETTINGS_FILE]
    copied = 0
    for filename in files_to_backup:
        if os.path.exists(filename):
            backup_name = f"backup_{timestamp}_{filename}"
            try:
                shutil.copy2(filename, backup_name)
                print(f"백업 완료: {backup_name}")
                copied += 1
            except OSError as error:
                print(f"{filename} 백업 실패: {error}")
    if copied == 0:
        print("백업할 데이터 파일이 없습니다.")


def restore_data():
    filename = input("\n복원할 백업 파일 경로: ").strip().strip('"')
    if not filename or not os.path.isfile(filename):
        print("파일을 찾을 수 없습니다.")
        return
    try:
        with open(filename, "r", encoding="utf-8") as file:
            restored = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("백업 파일을 읽을 수 없습니다.")
        return

    if filename.endswith(FILE_NAME):
        if not isinstance(restored, list) or not all(isinstance(item, dict) for item in restored):
            print("공부 기록 백업 형식이 올바르지 않습니다.")
            return
        target = FILE_NAME
    elif filename.endswith(SETTINGS_FILE):
        if not isinstance(restored, dict):
            print("설정 백업 형식이 올바르지 않습니다.")
            return
        target = SETTINGS_FILE
    else:
        print("study_data.json 또는 study_settings.json 백업 파일을 선택해 주세요.")
        return

    confirm = input(f"{target} 파일을 백업 내용으로 교체할까요? (y/n): ").strip().lower()
    if confirm != "y":
        print("복원을 취소했습니다.")
        return
    try:
        shutil.copy2(filename, target)
        print(f"{target} 복원이 완료되었습니다. 프로그램을 다시 실행하면 반영됩니다.")
    except OSError as error:
        print(f"복원에 실패했습니다: {error}")


def main():
    data = load_data()
    settings = load_settings()

    while True:
        print("\n========== STUDY MANAGER 3.0 ==========")
        print("1. 공부 기록 추가")
        print("2. 공부 기록 조회")
        print("3. 총 공부 시간 확인")
        print("4. 과목별 공부 시간 통계")
        print("5. 공부 기록 삭제")
        print("6. 공부 기록 수정")
        print("7. 공부 기록 검색")
        print("8. 주간·월간 통계")
        print("9. 하루 공부 목표 설정")
        print("10. 오늘의 목표 달성 현황")
        print("11. 연속 학습일 확인")
        print("12. CSV 파일로 내보내기")
        print("13. 오늘의 학습 요약")
        print("14. 과목별 주간 목표 설정")
        print("15. 과목별 주간 목표 현황")
        print("16. 데이터 백업")
        print("17. 백업 데이터 복원")
        print("0. 종료")

        choice = input("\n메뉴 선택: ").strip()
        if choice == "1":
            add_study(data)
        elif choice == "2":
            show_study(data)
        elif choice == "3":
            show_total(data)
        elif choice == "4":
            show_subject_stats(data)
        elif choice == "5":
            delete_study(data)
        elif choice == "6":
            edit_study(data)
        elif choice == "7":
            search_study(data)
        elif choice == "8":
            show_period_stats(data)
        elif choice == "9":
            set_daily_goal(settings)
        elif choice == "10":
            show_daily_goal(data, settings)
        elif choice == "11":
            show_streak(data)
        elif choice == "12":
            export_csv(data)
        elif choice == "13":
            show_today_summary(data)
        elif choice == "14":
            set_subject_goal(settings)
        elif choice == "15":
            show_subject_goals(data, settings)
        elif choice == "16":
            backup_data()
        elif choice == "17":
            restore_data()
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해 주세요.")


if __name__ == "__main__":
    main()
