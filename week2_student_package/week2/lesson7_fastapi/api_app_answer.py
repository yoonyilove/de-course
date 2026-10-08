from pathlib import Path
import pandas as pd
from fastapi import FastAPI, Query

def find_summary_path():
    here = Path(__file__).resolve()
    candidates = [
        here.parents[1] / "outputs" / "member_activity_summary.csv",
        Path.cwd() / "course_materials" / "week2" / "outputs" / "member_activity_summary.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("member_activity_summary.csv가 없습니다. prepare_api_data.py를 먼저 실행하세요.")

summary_path = find_summary_path()
summary = pd.read_csv(summary_path)

app = FastAPI(title="Matchmaking Activity API")

@app.get("/health")
def health():
    return {"status": "ok", "rows": len(summary)}

@app.get("/members")
def get_members(limit: int = Query(5, ge=1, le=100)):
    rows = summary.head(limit)
    safe_rows = rows.astype(object).where(pd.notna(rows), None)
    return safe_rows.to_dict(orient="records")
