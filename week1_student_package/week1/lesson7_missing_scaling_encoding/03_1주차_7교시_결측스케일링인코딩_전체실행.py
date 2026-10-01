"""1주차 7교시 전체 실행본: 결측·스케일링·인코딩."""

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
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
members = pd.read_csv(DATA_DIR / "matchmaking_members.csv").drop_duplicates("member_id", keep="first").copy()
preferences = pd.read_csv(DATA_DIR / "matchmaking_preferences.csv")
members["residence_region"] = members["residence_region"].str.strip().replace({"Seoul":"서울", "seoul":"서울"})
members["annual_income_10k_krw"] = pd.to_numeric(members["annual_income_10k_krw"], errors="coerce")
joined = pd.merge(members, preferences, on="member_id", how="left", validate="one_to_one")
num = ["age","annual_income_10k_krw","profile_completion_rate","recommendation_response_rate_prior","consultation_count_prior","pref_income_min_10k_krw","preference_strictness"]
cat = ["gender","residence_region","occupation_type","membership_tier","signup_channel","pref_education_min","deal_breakers"]
X,y = joined[num+cat], joined["meeting_scheduled"]
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
pre=ColumnTransformer([("num",Pipeline([("imputer",SimpleImputer(strategy="median")),("scaler",StandardScaler())]),num),("cat",Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore",sparse_output=False))]),cat)])
tr=pre.fit_transform(X_train); te=pre.transform(X_test)
print(tr.shape,te.shape)
assert tr.shape[0]==800 and te.shape[0]==200 and tr.shape[1]==te.shape[1] and np.isnan(tr).sum()==0
