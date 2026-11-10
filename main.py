import csv
import json
import os
from datetime import date, datetime, timedelta

FILE_NAME = "study_data.json"
SETTINGS_FILE = "study_settings.json"


def load_data():
    """기존 공부 기록을 불러옵니다."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("공부 기록 파일을 읽을 수 없습니다. 파일을 확인해 주세요.")
        return []


def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"daily_goal": 3.0}

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)
            return settings if isinstance(settings, dict) else {"daily_goal": 3.0}
    except (json.JSONDecodeError, OSError):
        print("설정 파일을 읽을 수 없어 기본 목표 시간 3시간을 사용합니다.")
        return {"daily_goal": 3.0}


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)


def input_date(prompt, default=None):
    """YYYY-MM-DD 형식의 날짜를 입력받습니다."""
    while True:
        value = input(prompt).strip()

        if not value and default:
            return default

        try:
            return date.fromisoformat(value).isoformat()
        except ValueError:
            print("날짜는 YYYY-MM-DD 형식으로 입력해 주세요. 예: 2026-11-10")


def input_hours(prompt):
    while True:
        try:
            hours = float(input(prompt))
            if hours <= 0:
                print("공부 시간은 0보다 커야 합니다.")
                continue
            return round(hours, 2)
        except ValueError:
            print("숫자로 입력해 주세요.")


def add_study(data):
    print("\n[ 공부 기록 추가 ]")
    subject = input("과목명: ").strip()
    if not subject:
        print("과목명을 입력해 주세요.")
        return

    hours = input_hours("공부 시간(시간): ")
    memo = input("공부 내용: ").strip()

    record = {
        "date": date.today().isoformat(),
        "subject": subject,
        "hours": hours,
        "memo": memo
    }
    data.append(record)
    save_data(data)
    print("공부 기록이 저장되었습니다!")


def show_study(data):
    if not data:
        print("등록된 공부 기록이 없습니다.")
        return

    print("\n[ 공부 기록 목록 ]")
    for index, record in enumerate(data, 1):
        print(f"\n{index}. 날짜: {record.get('date', '날짜 정보 없음')}")
        print(f"   과목: {record.get('subject', '과목 정보 없음')}")
        print(f"   시간: {record.get('hours', 0)}시간")
        print(f"   내용: {record.get('memo', '')}")


def show_total(data):
    total = sum(float(record.get("hours", 0)) for record in data)
    print(f"\n누적 공부 시간: {total:.1f}시간")


def show_subject_stats(data):
    if not data:
        print("등록된 공부 기록이 없습니다.")
        return

    stats = {}
    for record in data:
        subject = record.get("subject", "기타")
        stats[subject] = stats.get(subject, 0) + float(record.get("hours", 0))

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
        if number < 1 or number > len(data):
            print("올바른 번호를 입력해 주세요.")
            return

        deleted = data.pop(number - 1)
        save_data(data)
        print(f"{deleted.get('subject', '공부')} 기록이 삭제되었습니다.")
    except ValueError:
        print("숫자로 입력해 주세요.")


def edit_study(data):
    if not data:
        print("수정할 기록이 없습니다.")
        return

    show_study(data)
    try:
        number = int(input("\n수정할 기록 번호: "))
        if number < 1 or number > len(data):
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

    current_hours = record.get("hours", 0)
    while True:
        value = input(f"공부 시간 [{current_hours}]: ").strip()
        if not value:
            break
        try:
            hours = float(value)
            if hours <= 0:
                print("공부 시간은 0보다 커야 합니다.")
                continue
            record["hours"] = round(hours, 2)
            break
        except ValueError:
            print("숫자로 입력해 주세요.")

    memo = input(f"공부 내용 [{record.get('memo', '')}]: ").strip()
    if memo:
        record["memo"] = memo

    current_date = record.get("date", date.today().isoformat())
    new_date = input(f"공부 날짜 [{current_date}] (YYYY-MM-DD): ").strip()
    if new_date:
        try:
            record["date"] = date.fromisoformat(new_date).isoformat()
        except ValueError:
            print("날짜 형식이 올바르지 않아 기존 날짜를 유지합니다.")

    save_data(data)
    print("공부 기록이 수정되었습니다.")


def search_study(data):
    if not data:
        print("검색할 기록이 없습니다.")
        return

    keyword = input("\n검색할 과목명 또는 메모: ").strip().lower()
    if not keyword:
        print("검색어를 입력해 주세요.")
        return

    results = [
        record for record in data
        if keyword in record.get("subject", "").lower()
        or keyword in record.get("memo", "").lower()
        or keyword in record.get("date", "")
    ]

    if not results:
        print("검색 결과가 없습니다.")
        return

    print(f"\n[ 검색 결과: {len(results)}건 ]")
    for index, record in enumerate(results, 1):
        print(
            f"{index}. {record.get('date')} | {record.get('subject')} | "
            f"{record.get('hours')}시간 | {record.get('memo', '')}"
        )


def show_period_stats(data):
    print("\n[ 기간별 공부 통계 ]")
    print("1. 이번 주")
    print("2. 이번 달")
    choice = input("선택: ").strip()
    today = date.today()

    if choice == "1":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        title = f"{start} ~ {end}"
    elif choice == "2":
        start = today.replace(day=1)
        title = today.strftime("%Y년 %m월")
        end = today
    else:
        print("올바른 메뉴를 선택해 주세요.")
        return

    filtered = []
    for record in data:
        try:
            record_day = date.fromisoformat(record.get("date", ""))
            if start <= record_day <= end:
                filtered.append(record)
        except ValueError:
            continue

    total = sum(float(record.get("hours", 0)) for record in filtered)
    days = len({record.get("date") for record in filtered})
    print(f"\n기간: {title}")
    print(f"공부 기록: {len(filtered)}건")
    print(f"공부한 날짜: {days}일")
    print(f"총 공부 시간: {total:.1f}시간")

    if filtered:
        stats = {}
        for record in filtered:
            subject = record.get("subject", "기타")
            stats[subject] = stats.get(subject, 0) + float(record.get("hours", 0))
        print("과목별 시간:")
        for subject, hours in sorted(stats.items(), key=lambda item: item[1], reverse=True):
            print(f"- {subject}: {hours:.1f}시간")


def set_daily_goal(settings):
    current = settings.get("daily_goal", 3.0)
    print(f"\n현재 하루 공부 목표: {current}시간")
    try:
        goal = float(input("새로운 하루 목표 시간: "))
        if goal <= 0:
            print("목표 시간은 0보다 커야 합니다.")
            return
        settings["daily_goal"] = round(goal, 2)
        save_settings(settings)
        print(f"하루 공부 목표를 {goal:.1f}시간으로 설정했습니다.")
    except ValueError:
        print("숫자로 입력해 주세요.")


def show_daily_goal(data, settings):
    today = date.today().isoformat()
    today_hours = sum(
        float(record.get("hours", 0))
        for record in data if record.get("date") == today
    )
    goal = float(settings.get("daily_goal", 3.0))
    remaining = max(goal - today_hours, 0)

    print("\n[ 오늘의 공부 목표 ]")
    print(f"목표 시간: {goal:.1f}시간")
    print(f"실제 공부: {today_hours:.1f}시간")
    if remaining > 0:
        print(f"목표까지 남은 시간: {remaining:.1f}시간")
    else:
        print(f"목표 달성! 초과 공부: {today_hours - goal:.1f}시간")


def show_streak(data):
    study_days = set()
    for record in data:
        try:
            study_days.add(date.fromisoformat(record.get("date", "")))
        except ValueError:
            continue

    if not study_days:
        print("아직 공부 기록이 없습니다.")
        return

    today = date.today()
    check_day = today if today in study_days else today - timedelta(days=1)
    streak = 0

    while check_day in study_days:
        streak += 1
        check_day -= timedelta(days=1)

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
            for record in data:
                writer.writerow([
                    record.get("date", ""),
                    record.get("subject", ""),
                    record.get("hours", 0),
                    record.get("memo", "")
                ])
        print(f"CSV 파일로 저장했습니다: {filename}")
    except OSError as error:
        print(f"CSV 파일 저장에 실패했습니다: {error}")


def main():
    data = load_data()
    settings = load_settings()

    while True:
        print("\n========== STUDY MANAGER 2.0 ==========")
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
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택해 주세요.")


if __name__ == "__main__":
    main()
