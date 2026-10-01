"""1주차 4교시 전체 실행본: Pandas 건강검진."""

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
members = pd.read_csv(DATA_DIR / "matchmaking_members.csv")
print(members.head(3))
print(members.shape)
print(members.columns.tolist())
members.info()
print(members.dtypes[["age","annual_income_10k_krw","meeting_scheduled"]])
print(members.isna().sum().sort_values(ascending=False).head())
print(members[["age","profile_completion_rate","profile_views_30d"]].describe())
print(type(members["age"]), type(members[["age","residence_region"]]))
print(members.loc[members["is_active"], ["member_id","name","login_week1"]].head(3))
print(members.iloc[2:7, 0:4])
new_members = pd.read_csv(DATA_DIR / "matchmaking_members_new.csv")
assert new_members.shape == (100,21)
