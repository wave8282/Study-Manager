"""Study Manager 4.0 - 모듈형 개인 학습 관리 프로그램."""
from datetime import date, timedelta
from storage import JSONStorage
from study_service import StudyService
from analytics import subject_totals, period_summary, current_streak, today_summary
from goal_manager import GoalManager
from backup_manager import create_backup, restore_backup
from export_manager import export_records

DATA_FILE = "study_data.json"
SETTINGS_FILE = "study_settings.json"

data_store = JSONStorage(DATA_FILE, [])
records = data_store.load()
if not isinstance(records, list):
    print("[경고] 공부 기록 파일 형식이 올바르지 않아 빈 목록으로 시작합니다.")
    records = []
records = [row for row in records if isinstance(row, dict)]
service = StudyService(records, data_store.save)
goals = GoalManager(SETTINGS_FILE)


def pause():
    input("\nEnter를 누르면 메뉴로 돌아갑니다...")


def show_records(rows=None):
    rows = records if rows is None else rows
    if not rows:
        print("등록된 공부 기록이 없습니다.")
        return
    print("\n[ 공부 기록 ]")
    for number, row in enumerate(rows, 1):
        print(f"{number:>3}. {row.get('date','')} | {row.get('subject','')} | "
              f"{row.get('hours',0)}시간 | {row.get('memo','')}")


def choose_index():
    show_records()
    if not records:
        return None
    try:
        number = int(input("기록 번호: "))
        if 1 <= number <= len(records):
            return number - 1
    except ValueError:
        pass
    print("올바른 번호를 입력해 주세요.")
    return None


def add_record():
    print("\n[ 공부 기록 추가 ]")
    subject = input("과목명: ").strip()
    hours = input("공부 시간(시간): ").strip()
    memo = input("공부 내용: ").strip()
    study_date = input(f"날짜 [기본값 {date.today().isoformat()}]: ").strip() or None
    try:
        row = service.add(subject, hours, memo, study_date)
        print(f"저장 완료: {row['subject']} {row['hours']}시간")
    except ValueError as error:
        print(f"입력 오류: {error}")


def edit_record():
    index = choose_index()
    if index is None:
        return
    row = records[index]
    print("변경하지 않을 항목은 Enter를 누르세요.")
    subject = input(f"과목명 [{row.get('subject','')}]: ").strip()
    hours = input(f"공부 시간 [{row.get('hours',0)}]: ").strip()
    memo = input(f"공부 내용 [{row.get('memo','')}]: ").strip()
    study_date = input(f"날짜 [{row.get('date','')}]: ").strip()
    changes = {}
    if subject: changes["subject"] = subject
    if hours: changes["hours"] = hours
    if memo: changes["memo"] = memo
    if study_date: changes["date"] = study_date
    try:
        service.update(index, **changes)
        print("기록을 수정했습니다.")
    except ValueError as error:
        print(f"수정 실패: {error}")


def delete_record():
    index = choose_index()
    if index is None:
        return
    if input("정말 삭제할까요? (y/n): ").strip().lower() != "y":
        print("삭제를 취소했습니다.")
        return
    removed = service.delete(index)
    print(f"{removed.get('subject','')} 기록을 삭제했습니다.")


def show_statistics():
    print("\n[ 전체 과목별 공부 시간 ]")
    totals = subject_totals(records)
    if not totals:
        print("기록이 없습니다.")
    for subject, hours in totals.items():
        print(f"- {subject}: {hours:.1f}시간")
    print(f"누적 공부 시간: {sum(totals.values()):.1f}시간")


def show_period():
    print("\n1. 이번 주  2. 이번 달")
    choice = input("선택: ").strip()
    today = date.today()
    if choice == "1":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
    elif choice == "2":
        start = today.replace(day=1)
        end = today
    else:
        print("잘못된 선택입니다.")
        return
    result = period_summary(records, start, end)
    print(f"\n기간: {start} ~ {end}")
    print(f"기록 {result['records']}건 | 공부한 날짜 {result['days']}일 | 총 {result['hours']:.1f}시간")
    for subject, hours in result["subjects"].items():
        print(f"- {subject}: {hours:.1f}시간")


def show_today():
    result = today_summary(records)
    status = goals.daily_status(result["hours"])
    print("\n[ 오늘의 학습 요약 ]")
    print(f"기록 {result['count']}건 | 과목 {len(result['subjects'])}개")
    print(f"공부 시간 {result['hours']:.1f} / 목표 {status['goal']:.1f}시간")
    print(f"목표 달성률: {status['percent']:.1f}%")
    print(f"남은 시간: {status['remaining']:.1f}시간")
    for subject, hours in result["subjects"].items():
        print(f"- {subject}: {hours:.1f}시간")


def set_daily_goal():
    value = input("하루 공부 목표 시간: ").strip()
    try:
        goals.set_daily_goal(value)
        print("하루 목표를 저장했습니다.")
    except ValueError as error:
        print(error)


def set_subject_goal():
    subject = input("과목명: ").strip()
    value = input("주간 목표 시간: ").strip()
    try:
        goals.set_subject_goal(subject, value)
        print(f"{subject} 주간 목표를 저장했습니다.")
    except ValueError as error:
        print(error)


def show_subject_goals():
    today = date.today()
    start = today - timedelta(days=today.weekday())
    summary = period_summary(records, start, start + timedelta(days=6))
    statuses = goals.subject_status(summary["subjects"])
    if not statuses:
        print("설정된 과목별 목표가 없습니다.")
        return
    print("\n[ 과목별 주간 목표 ]")
    for subject, item in statuses.items():
        print(f"{subject}: {item['studied']:.1f}/{item['goal']:.1f}시간 "
              f"({item['percent']:.1f}%) · 남은 시간 {item['remaining']:.1f}시간")


def show_study_streak():
    streak, total_days = current_streak(records)
    print(f"현재 연속 학습일: {streak}일")
    print(f"누적 학습일: {total_days}일")


def search_records():
    keyword = input("검색어(과목·날짜·내용): ")
    results = service.search(keyword)
    if not results:
        print("검색 결과가 없습니다.")
        return
    print(f"검색 결과 {len(results)}건")
    for index, row in results:
        print(f"{index + 1}. {row.get('date')} | {row.get('subject')} | "
              f"{row.get('hours')}시간 | {row.get('memo','')}")


def backup():
    try:
        created = create_backup([DATA_FILE, SETTINGS_FILE])
        if created:
            print("백업 완료:")
            for path in created:
                print(f"- {path}")
        else:
            print("백업할 데이터 파일이 없습니다.")
    except OSError as error:
        print(f"백업 실패: {error}")


def restore():
    print("복원할 백업 파일 경로를 입력하세요. 예: backups/20261110_210000_study_data.json")
    source = input("백업 파일: ").strip().strip('"')
    if source.endswith("study_data.json"):
        target = DATA_FILE
    elif source.endswith("study_settings.json"):
        target = SETTINGS_FILE
    else:
        print("파일명 끝이 study_data.json 또는 study_settings.json이어야 합니다.")
        return
    if input(f"{target} 파일을 교체할까요? (y/n): ").strip().lower() != "y":
        print("복원을 취소했습니다.")
        return
    try:
        restore_backup(source, target)
        print("복원 완료. 변경사항을 반영하려면 프로그램을 다시 실행하세요.")
    except (OSError, ValueError) as error:
        print(f"복원 실패: {error}")


def export_csv():
    if not records:
        print("내보낼 기록이 없습니다.")
        return
    filename = f"study_records_{date.today().isoformat()}.csv"
    try:
        path = export_records(records, filename)
        print(f"CSV 내보내기 완료: {path}")
    except OSError as error:
        print(f"내보내기 실패: {error}")


def main():
    menu = {
        "1": ("공부 기록 추가", add_record),
        "2": ("공부 기록 조회", show_records),
        "3": ("공부 기록 수정", edit_record),
        "4": ("공부 기록 삭제", delete_record),
        "5": ("과목·날짜·내용 검색", search_records),
        "6": ("전체 과목별 통계", show_statistics),
        "7": ("주간·월간 통계", show_period),
        "8": ("오늘의 학습 요약 및 목표 현황", show_today),
        "9": ("하루 공부 목표 설정", set_daily_goal),
        "10": ("과목별 주간 목표 설정", set_subject_goal),
        "11": ("과목별 주간 목표 현황", show_subject_goals),
        "12": ("연속 학습일 확인", show_study_streak),
        "13": ("CSV 파일 내보내기", export_csv),
        "14": ("데이터 백업", backup),
        "15": ("백업 데이터 복원", restore),
    }
    while True:
        print("\n========== STUDY MANAGER 4.0 ==========")
        for key, (label, _) in menu.items():
            print(f"{key}. {label}")
        print("0. 종료")
        choice = input("\n메뉴 선택: ").strip()
        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        action = menu.get(choice)
        if action:
            action[1]()
        else:
            print("잘못된 메뉴 번호입니다.")


if __name__ == "__main__":
    main()
