# Study Manager 4.0 📚

Python 표준 라이브러리로 만든 개인 학습 기록 관리 프로그램입니다. 4.0에서는 하나의 긴 파일에 모여 있던 기능을 역할별 모듈로 분리해 유지보수와 테스트가 쉬운 구조로 개선했습니다.

## 주요 기능
- 공부 기록 추가·조회·수정·삭제
- 과목·날짜·메모 검색
- 전체 과목별 학습 시간 통계
- 주간·월간 학습 통계
- 오늘의 학습 요약 및 목표 달성률
- 하루 공부 목표와 과목별 주간 목표 설정
- 연속 학습일 및 누적 학습일 계산
- CSV 내보내기
- JSON 데이터 백업 및 검증 후 복원
- 입력값 검증 및 안전한 JSON 저장
- unittest 기반 핵심 기능 자동 테스트

## 프로젝트 구조
```text
Study-Manager/
├── main.py                    # 프로그램 실행 및 메뉴
├── storage.py                 # JSON 파일 저장·로드
├── validators.py              # 날짜·시간·문자열 검증
├── study_service.py           # 공부 기록 CRUD 및 검색
├── analytics.py               # 통계·연속 학습일 계산
├── goal_manager.py             # 하루·과목별 목표 관리
├── backup_manager.py           # 백업 및 복원
├── export_manager.py           # CSV 내보내기
├── tests/
│   └── test_study_manager.py   # 자동 테스트
├── study_data.json             # 실행 시 자동 생성되는 공부 기록
└── study_settings.json         # 실행 시 자동 생성되는 목표 설정
```

## 실행 방법
Python 3.10 이상을 권장합니다. 외부 패키지는 필요하지 않습니다.

```bash
python main.py
```

## 자동 테스트
프로젝트 최상위 폴더에서 실행합니다.

```bash
python -m unittest discover -s tests -v
```

## 기존 데이터 호환
기존 버전에서 사용하던 `study_data.json`과 `study_settings.json`을 같은 폴더에 두면 계속 사용할 수 있습니다. 업데이트 전에 파일을 별도 복사해 백업하는 것을 권장합니다.

## 기술 요소
Python 함수·모듈·클래스, JSON 및 CSV 파일 입출력, 예외 처리, 날짜 계산, 단위 테스트를 활용했습니다.
