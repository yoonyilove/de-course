# 3주차 학생용 먼저 읽기

이번 주차는 주피터 노트북을 배포하지 않습니다. 각 교시의 학생용 `.py` 파일에서 `___` 빈칸을 채운 뒤, Python 또는 Streamlit으로 실행합니다.

## 압축을 푼 뒤 지킬 것

압축을 풀어 생긴 `week3_student_package` 폴더 전체를 VS Code 또는 Cursor에서 엽니다. `course_materials` 안의 `week3` 폴더나 파일 하나만 따로 옮기지 않습니다.

```text
week3_student_package/
├── course_materials/
│   ├── matchmaking_data/03_week3/
│   └── week3/
├── requirements.txt
└── README_먼저읽기.md
```

데이터와 전처리기 파일의 위치가 이 구조에 맞아야 `week3_common.py`가 경로를 찾을 수 있습니다.

## 처음 한 번만 할 일

터미널에서 `week3_student_package` 폴더로 이동한 뒤 `de-course` 환경을 활성화하고, 필요한 패키지를 설치합니다.

```bash
cd week3_student_package
conda activate de-course
python -m pip install -r requirements.txt
cd course_materials
```

이미 필요한 패키지가 설치되어 있다면 설치 명령을 매번 다시 실행하지 않아도 됩니다.

## 학생에게 제공되는 파일 목록

### 공통 실행 자료

- `course_materials/week3/week3_common.py` — 공통 경로·전처리·그래프·DB 지원 함수
- `course_materials/week3/support_api.py` — 1교시와 대시보드가 사용할 로컬 지원 API
- `course_materials/week3/artifacts/matchmaking_preprocessor.joblib` — 2주차에서 학습해 저장한 전처리기
- `course_materials/matchmaking_data/03_week3/api_members_fallback.csv` — API가 어려울 때 사용할 100행 대체 CSV
- `course_materials/matchmaking_data/03_week3/README.md` — 3주차 데이터 설명
- `course_materials/matchmaking_data/03_week3/data_dictionary_week3.csv` — 열 이름과 뜻

### 정규 수업 학생용 코드

- 1교시 `lesson1_api_collect/3_1_api_collect_student.py`
- 2교시 `lesson2_streamlit_basics/3_2_streamlit_app_basics_student.py`
- 3교시 `lesson3_apply_pipeline/3_3_preprocessing_app_student.py`
- 4교시 `lesson4_sqlite/3_4_sqlite_student.py`
- 5교시 `lesson5_eda_charts/3_5_eda_charts_student.py`
- 6교시 `lesson6_pca/3_6_pca_student.py`
- 7교시 `lesson7_integrated_dashboard/3_7_operations_dashboard_student.py`
- 8교시 `lesson8_capstone/final_app_student.py`

1교시의 Mac·Windows 터미널 명령은 `lesson1_api_collect` 안의 실행명령 파일에도 들어 있습니다.

### 선택 보충 자료

9교시는 정규 3주차가 끝난 뒤 시간이 남을 때 사용하는 선택 보충입니다.

- `lesson9_optional_streamlit_filters_download/3주차_9교시_학생용_대시보드.py`
- 선택 보충 화면 예시 PNG 2개

## 교시별 실행 순서

### 1교시: API 서버를 먼저 켭니다

`course_materials` 폴더에서 다음 명령을 실행합니다. 위의 준비 명령까지 마쳤다면 이미 이 폴더에 들어와 있습니다.

```bash
conda activate de-course
python -m uvicorn week3.support_api:app --host 127.0.0.1 --port 8000
```

터미널에 `Uvicorn running on http://127.0.0.1:8000`이 보이면 서버가 실행 중입니다. 브라우저에서 `http://127.0.0.1:8000/health`를 열어 `rows`가 100인지 확인합니다.

API 서버를 실행한 터미널은 닫지 않습니다. 다른 터미널에서 다음 명령으로 1교시 학생용 파일을 실행합니다.

```bash
python week3/lesson1_api_collect/3_1_api_collect_student.py
```

### 2·3·7·8교시: Streamlit 화면을 실행합니다

API를 사용하는 교시는 API 터미널을 계속 켜 둔 상태에서 두 번째 터미널을 사용합니다.

```bash
python -m streamlit run week3/lesson2_streamlit_basics/3_2_streamlit_app_basics_student.py
```

교시에 따라 파일 경로만 바꿉니다.

```bash
python -m streamlit run week3/lesson3_apply_pipeline/3_3_preprocessing_app_student.py
python -m streamlit run week3/lesson7_integrated_dashboard/3_7_operations_dashboard_student.py
python -m streamlit run week3/lesson8_capstone/final_app_student.py
```

Streamlit이 안내한 `http://localhost:8501` 또는 `http://127.0.0.1:8501` 주소를 브라우저에서 엽니다. 실행을 끝낼 때는 Streamlit 터미널에서 `Control+C`를 누릅니다.

### 4·5·6교시: Python 파일을 실행합니다

빈칸을 채우고 저장한 뒤 `course_materials` 폴더에서 다음처럼 실행합니다.

```bash
python week3/lesson4_sqlite/3_4_sqlite_student.py
python week3/lesson5_eda_charts/3_5_eda_charts_student.py
python week3/lesson6_pca/3_6_pca_student.py
```

결과는 터미널에 출력되고, CSV·SQLite·PNG 결과는 `course_materials/week3/outputs` 아래에 만들어집니다.

## 빈칸을 채우는 방법

- 화면에 표시되는 제목·버튼 문구와 직접 만든 변수명은 이미 제공되어 있습니다.
- 함수·메서드·속성·설정값·열 선택 부분에 있는 `___`를 앞 교시에서 배운 방식으로 채웁니다.
- 빈칸을 채우기 전에는 예상 결과를 먼저 적어 봅니다.
- 서버·Streamlit 교시는 터미널이 실행 중인 상태에서 파일을 저장하면 화면을 새로고침해 결과를 확인합니다.

## 학생에게 제공하지 않는 파일

이번 배포본에는 수업 슬라이드, 강사용 정답, 전체실행 파일, 복습완성본, 강사용 노트북을 넣지 않았습니다. 수업 중 안내된 학생용 `.py` 파일과 공통 실행 자료만 사용합니다.

## 문제가 생겼을 때

- `FileNotFoundError`: `week3_student_package` 안의 `course_materials` 폴더 전체를 VS Code에서 열었는지 확인합니다.
- `NameError`에 `___`: 해당 빈칸을 아직 채우지 않았거나 저장하지 않은 상태입니다.
- `ConnectionError`: 1교시 API 서버가 실행 중인지, 주소와 포트가 8000인지 확인합니다.
- `Port 8000 is already in use`: 이전 API 터미널에서 `Control+C`를 누른 뒤 다시 실행합니다.
- Streamlit 화면이 예전 내용이면 파일을 저장한 뒤 브라우저를 새로고침합니다.
