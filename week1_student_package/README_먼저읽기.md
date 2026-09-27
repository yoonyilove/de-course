# 1주차 학생용 자료

이 폴더는 1주차 수업을 시작할 때 학생에게 처음 전달하는 자료입니다.
`outputs` 폴더, 강사용 정답 파일, 수업 슬라이드는 포함하지 않았습니다.

## 1. 폴더를 먼저 열어 주세요

압축을 풀었다면 **`week1_student_package` 폴더 자체**를 VS Code 또는 Cursor에서 엽니다.
`week1` 폴더만 따로 열지 말고, 이 폴더를 프로젝트 폴더로 선택해 주세요.

GitHub에서 `Download ZIP`으로 받으면 바깥 폴더 이름에 저장소 이름과 `-main`이 붙을 수
있습니다. 예를 들어 `python-data-engineering-course-3weeks-main`처럼 보이는 것은 정상입니다.
그 안에서 바로 `week1`, `matchmaking_data`, `setup`, `requirements.txt`가 보이는 폴더를
프로젝트 폴더로 엽니다. 폴더 이름은 달라도 이 네 항목이 바로 들어 있으면 됩니다.

그 안에는 다음 항목이 있습니다.

- `setup`: 설치 안내와 환경 점검
- `matchmaking_data/01_week1`: 수업 데이터
- `week1`: 1~8교시 학생용 지적실험노트
- `requirements.txt`: 필요한 Python 패키지 목록

## 2. 처음 한 번만 환경을 점검합니다

터미널에서 이 폴더를 현재 위치로 둔 뒤 다음 명령을 실행합니다.

```bash
python setup/02_1주차_환경점검.py
```

모든 항목이 `PASS`인지 확인합니다. `FAIL`이 있으면 수업을 시작하기 전에
`setup/01_MacBook_완전초보_설정.md`(Mac) 또는
`setup/01_Surface_Windows_완전초보_설정.md`(Windows)를 먼저 따라갑니다.

## 3. 노트북을 여는 순서

교시가 시작되면 해당 폴더의 **`학생용_지적실험노트.ipynb`**만 엽니다.

1. VS Code/Cursor에서 `week1` 폴더를 펼칩니다.
2. 현재 교시의 `학생용_지적실험노트.ipynb`를 엽니다.
3. 커널에서 `Python (de-course)`를 선택합니다.
4. 준비 셀을 먼저 실행합니다.
5. `FILL_ME` 또는 빈칸만 직접 채우고, 결과를 예상한 뒤 실행합니다.

완성된 복습본은 처음부터 제공하지 않습니다. 각 교시가 끝난 뒤 강사가 안내한 시점에
별도로 받습니다.

## 4. 데이터는 언제 처음 사용하나요?

- 1~3교시: 노트북 안의 작은 Python·NumPy 연습 자료를 사용합니다.
- 4교시: `matchmaking_members.csv`를 처음 읽습니다.
- 5~7교시: 같은 1주차 CSV와 선호조건 CSV를 이어서 사용합니다.
- 8교시: `matchmaking_members_new.csv`를 새 회원 데이터로 사용합니다.

데이터 파일의 설명은 `matchmaking_data/01_week1/1주차_데이터_열이름과뜻_안내슬라이드.pptx`에서 확인합니다.

## 5. 파일을 옮기거나 이름을 바꾸지 마세요

노트북은 데이터 폴더를 자동으로 찾도록 준비되어 있습니다. 그래도 아래 구조와 파일명은
그대로 유지해야 합니다.

```text
week1_student_package/
├── matchmaking_data/01_week1/
│   ├── matchmaking_members.csv
│   ├── matchmaking_preferences.csv
│   └── matchmaking_members_new.csv
└── week1/lesson1_list_type_flow/ ... lesson8_capstone/
```

오류가 나면 노트북 셀을 무작정 다시 만들지 말고, 먼저
`setup/03_오류별_구조대.md`의 증상별 안내를 확인합니다.
