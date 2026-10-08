from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query

BASE_DIR = Path(__file__).resolve().parent
summary = pd.FILL_ME(BASE_DIR / "outputs" / "FILL_ME")
app = FastAPI(title="FILL_ME")

@app.get("/health")
def health():
    return {"status": "FILL_ME", "rows": FILL_ME}

@app.get("/items")
def get_items(limit: int = Query(FILL_ME, ge=1, le=100)):
    rows = summary.head(limit)
    safe_rows = rows.astype(object).where(pd.notna(rows), None)
    return safe_rows.to_dict(orient="FILL_ME")
