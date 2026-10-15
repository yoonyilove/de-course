# 3주차 금융 개인·팀 프로젝트

## 이번 프로젝트에서 만드는 것

2주차 결과인 `finance_merchant_summary.csv`을 출발점으로 사용합니다.

```text
2주차 요약 CSV와 전처리기
→ 전처리 재사용과 PCA
→ SQLite 저장·SQL 확인
→ FastAPI 제공
→ Streamlit 필터·지표·그래프·다운로드
```

## 학생이 여는 순서

1. `3주차_금융_프로젝트_학생용.ipynb`
2. 노트북 Q1~Q5를 실행해 `outputs/finance_dashboard_ready.csv`을 만듭니다.
3. `api_app_student.py`의 `FILL_ME`를 채웁니다.
4. `dashboard_student.py`의 `FILL_ME`를 채웁니다.
5. 터미널 두 개에서 API와 Streamlit을 실행합니다.
6. 노트북 Q6의 인사이트 세 문장을 작성합니다.

## 시작 데이터

- `data/finance_merchant_summary.csv`: 240행×26열, 한 행은 가맹점 한 개
- `artifacts/finance_preprocessor.joblib`: 2주차 숫자·문자 처리 규칙을 저장한 객체
- 전처리 결과 열 수: 28개

학생이 2주차 과제를 완료했다면 이 두 파일을 자신의 결과로 교체해도 됩니다. 파일명과 열 이름은 그대로 유지합니다.

## 실행 명령

과제 폴더를 VS Code 또는 Cursor에서 연 뒤 터미널 1:

```bash
python -m uvicorn api_app_student:app --reload --host 127.0.0.1 --port 8010
```

터미널 2:

```bash
python -m streamlit run dashboard_student.py --server.port 8510
```

확인 주소:

- `http://127.0.0.1:8010/health`
- `http://127.0.0.1:8010/items?limit=3`
- `http://127.0.0.1:8510`

## 제출물

- 실행 결과가 남은 학생용 노트북
- `outputs/finance_dashboard_ready.csv`
- `database/finance_project.db`
- `figures/finance_pca.png`
- 완성한 `api_app_student.py`와 `dashboard_student.py`
- API `/health` 화면과 Streamlit 화면 캡처
- Q6 인사이트 세 문장

> manual_review_required는 수업용 운영 라벨이며 실제 신용·제재 결정을 대신하지 않습니다.
