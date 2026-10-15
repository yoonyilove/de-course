from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "outputs" / "finance_dashboard_ready.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(
        "먼저 3주차 프로젝트 노트북 Q1~Q5를 실행해 "
        "finance_dashboard_ready.csv을 만들어 주세요."
    )

data = pd.read_csv(DATA_PATH)
app = FastAPI(title="금융 가맹점 운영 API")


@app.get("FILL_ME")
def health():
    return {"status": "ok", "rows": len(data)}


@app.get("FILL_ME")
def get_items(
    limit: int = Query(FILL_ME, ge=1, le=300),
    segment: str | None = None,
):
    rows = data
    if segment:
        rows = rows[rows["industry"] == segment]
    rows = rows.head(limit)
    safe_rows = rows.astype(object).where(pd.notna(rows), None)
    return safe_rows.to_dict(orient="FILL_ME")
