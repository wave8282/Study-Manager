
import json
import os

FILE_NAME = "study_data.json"


# 데이터 불러오기
def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


# 데이터 저장하기
def save_data(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# 공부 기록 추가
def add_study(data):
    subject = input("과목명: ")
    hours = float(input("공부 시간(시간): "))
    memo = input("공부 내용: ")

    record = {
        "subject": subject,
        "hours": hours,
        "memo": memo
    }

    data.append(record)
    save_data(data)

    print("공부 기록이 저장되었습니다!")


# 공부 기록 조회
def show_study(data):
    if not data:
        print("등록된 공부 기록이 없습니다.")
        return

    print("\n[ 공부 기록 목록 ]")

    for i, record in enumerate(data, 1):
        print(f"{i}. 과목: {record['subject']}")
        print(f"   시간: {record['hours']}시간")
        print(f"   내용: {record['memo']}")


# 총 공부 시간 확인
def show_total(data):
    total = sum(record["hours"] for record in data)
    print(f"\n총 공부 시간: {total:.1f}시간")


# 프로그램 실행
def main():
    data = load_data()

    while True:
        print("\n===== STUDY MANAGER =====")
        print("1. 공부 기록 추가")
        print("2. 공부 기록 조회")
        print("3. 총 공부 시간 확인")
        print("0. 종료")

        choice = input("메뉴 선택: ")

        if choice == "1":
            add_study(data)

        elif choice == "2":
            show_study(data)

        elif choice == "3":
            show_total(data)

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 입력입니다.")


if __name__ == "__main__":
    main()
