"""2주차 7교시 전체 실행본: FastAPI."""

from pathlib import Path
import pandas as pd

def find_week2_data_dir():
    """노트북을 어느 교시 폴더에서 열어도 2주차 데이터 폴더를 찾습니다."""
    here = Path.cwd().resolve()
    for base in [here, *here.parents]:
        candidates = [
            base / "course_materials" / "matchmaking_data" / "02_week2",
            base / "matchmaking_data" / "02_week2",
            base / "02_week2",
        ]
        for candidate in candidates:
            if (candidate / "activity_batches").exists():
                return candidate
    raise FileNotFoundError("02_week2 데이터 폴더를 찾지 못했습니다. python_lecture 프로젝트 안에서 노트북을 열어 주세요.")

DATA_DIR = find_week2_data_dir()
WEEK2_DIR = DATA_DIR.parents[1] / "week2"
OUTPUT_DIR = WEEK2_DIR / "outputs"
print("데이터 폴더:", DATA_DIR)


# Q1. API가 돌려줄 데이터 모양을 작은 dict로 먼저 확인합니다
example_response = {
    "status": "ok",
    "rows": 1000,
}
print(example_response)


# Q2. 서버가 읽을 회원 요약 CSV가 준비되었는지 확인합니다
# 먼저 터미널에서 실행합니다.
# python prepare_api_data.py
summary_path = OUTPUT_DIR / "member_activity_summary.csv"
print(summary_path.exists())
summary = pd.read_csv(summary_path)
print(summary.shape)


# Q3. FastAPI 앱을 만들고 상태 확인 주소 /health를 연결합니다
# api_app_answer.py의 핵심 부분입니다.
from fastapi import FastAPI, Query
app = FastAPI(title="Matchmaking Activity API")

@app.get("/health")
def health():
    return {"status": "ok", "rows": len(summary)}


# Q4. 요청한 수만큼 회원 요약을 돌려주는 /members를 만듭니다
@app.get("/members")
def get_members(limit: int = Query(5, ge=1, le=100)):
    rows = summary.head(limit)
    safe_rows = rows.astype(object).where(pd.notna(rows), None)
    return safe_rows.to_dict(orient="records")


# Q5. 서버를 켜고 /docs와 자동 요청으로 응답을 확인합니다
# 터미널에서 실행할 명령
# uvicorn api_app_student:app --reload --port 8000

from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get("/health")
print(response.status_code, response.json())


print("[PASS] 2주차 7교시 전체 실행 완료")
