"""1주차 5교시 전체 실행본: 선택·정제·집계."""

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
members = pd.read_csv(DATA_DIR / "matchmaking_members.csv").copy()
members["residence_region"] = members["residence_region"].str.strip().replace({"Seoul":"서울", "seoul":"서울"})
income = pd.to_numeric(members["annual_income_10k_krw"], errors="coerce")
members["annual_income_10k_krw"] = income.fillna(income.median())
members = members.drop_duplicates("member_id", keep="first").copy()
selected = members.query("is_active == True and age >= 30")
login_cols = [f"login_week{i}" for i in range(1,5)]
members["login_total"] = members[login_cols].sum(axis=1)
report = members.groupby("residence_region").agg(member_count=("member_id","count"), avg_logins=("login_total","mean")).reset_index()
members["label_apply"] = members["login_total"].apply(lambda x: "활발" if x >= 10 else "일반")
members["label_where"] = np.where(members["login_total"] >= 10, "활발", "일반")
assert members.shape[0] == 1000
assert (members["label_apply"] == members["label_where"]).all()
print(selected.shape, report.head())
