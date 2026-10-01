"""1주차 6교시 전체 실행본: 결합·날짜·분할."""

from pathlib import Path
import numpy as np
import pandas as pd

def find_week1_data_dir():
    """어디에서 노트북을 열어도 수업 데이터 폴더를 찾습니다."""
    here = Path.cwd().resolve()
    for base in [here, *here.parents]:
        candidates = [
            base / "course_materials" / "matchmaking_data" / "01_week1",
            base / "matchmaking_data" / "01_week1",
            base / "01_week1",
        ]
        for candidate in candidates:
            if (candidate / "matchmaking_members.csv").exists():
                return candidate
    raise FileNotFoundError("matchmaking_members.csv를 찾지 못했습니다. 프로젝트 폴더 안에서 노트북을 열어 주세요.")

DATA_DIR = find_week1_data_dir()
print("데이터 폴더:", DATA_DIR)
from sklearn.model_selection import train_test_split
members = pd.read_csv(DATA_DIR / "matchmaking_members.csv").drop_duplicates("member_id", keep="first").copy()
members["annual_income_10k_krw"] = pd.to_numeric(members["annual_income_10k_krw"], errors="coerce")
preferences = pd.read_csv(DATA_DIR / "matchmaking_preferences.csv")
joined = pd.merge(members, preferences, on="member_id", how="left", validate="one_to_one")
joined["signup_dt"] = pd.to_datetime(joined["signup_datetime"], errors="coerce")
joined["signup_year"] = joined["signup_dt"].dt.year
joined["signup_month"] = joined["signup_dt"].dt.month
joined["signup_days"] = (pd.Timestamp("2026-09-01") - joined["signup_dt"]).dt.days
X = joined.drop(columns=["meeting_scheduled","member_id","name","signup_datetime","signup_dt"])
y = joined["meeting_scheduled"]
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
print(joined.shape, X_train.shape, X_test.shape)
assert joined.shape[0] == 1000 and len(X_test) == 200
