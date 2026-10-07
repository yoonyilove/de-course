"""1주차 8교시 전체 실행본: 신규 회원 종합실습."""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def find_week1_data_dir():
    here = Path.cwd().resolve()
    for base in [here, *here.parents]:
        for candidate in [
            base / "course_materials" / "matchmaking_data" / "01_week1",
            base / "matchmaking_data" / "01_week1",
            base / "01_week1",
        ]:
            if (candidate / "matchmaking_members_new.csv").exists():
                return candidate
    raise FileNotFoundError("01_week1 데이터 폴더를 찾지 못했습니다.")

DATA_DIR = find_week1_data_dir()
OUTPUT_DIR = DATA_DIR.parents[1] / "week1" / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
print("데이터 폴더:", DATA_DIR)


# Q1. 어떤 파일을 처리할지 먼저 확인합니다
new_path = DATA_DIR / "matchmaking_members_new.csv"
print(new_path.name)
print(new_path.exists())


# Q2. 신규회원 표의 크기와 상태를 확인합니다
new_members = pd.read_csv(new_path)
print(new_members.shape)
print("중복:", new_members.duplicated("member_id").sum())
print("결측:", new_members.isna().sum().sum())


# Q3. 기존 1,000명에서 전처리 기준을 다시 만듭니다
members = pd.read_csv(DATA_DIR / "matchmaking_members.csv")
members = members.drop_duplicates("member_id", keep="first").copy()
members["residence_region"] = members["residence_region"].str.strip().replace({"Seoul":"서울", "seoul":"서울"})
members["annual_income_10k_krw"] = pd.to_numeric(members["annual_income_10k_krw"], errors="coerce")
preferences = pd.read_csv(DATA_DIR / "matchmaking_preferences.csv")
joined = members.merge(preferences, on="member_id", how="left", validate="one_to_one")
print(joined.shape)


# Q4. 신규회원의 열을 기존 전처리 입력과 똑같이 맞춥니다
numeric_features = ["age","annual_income_10k_krw","profile_completion_rate","recommendation_response_rate_prior","consultation_count_prior","pref_income_min_10k_krw","preference_strictness"]
categorical_features = ["gender","residence_region","occupation_type","membership_tier","signup_channel","pref_education_min","deal_breakers"]
X = joined[numeric_features + categorical_features]
y = joined["meeting_scheduled"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
new_members["pref_income_min_10k_krw"] = np.nan
new_members["preference_strictness"] = X_train["preference_strictness"].median()
new_members["pref_education_min"] = X_train["pref_education_min"].mode().iloc[0]
new_members["deal_breakers"] = np.nan
new_X = new_members[numeric_features + categorical_features]
print(new_X.shape)


# Q5. 기준은 train에서 배우고 신규회원에는 적용만 합니다
numeric_pipe = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())])
categorical_pipe = Pipeline([("imputer", SimpleImputer(strategy="most_frequent")), ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))])
preprocessor = ColumnTransformer([("num", numeric_pipe, numeric_features), ("cat", categorical_pipe, categorical_features)])
train_processed = preprocessor.fit_transform(X_train)
new_processed = preprocessor.transform(new_X)
print(train_processed.shape, new_processed.shape)


# Q6. 처리 결과를 열 이름과 함께 CSV로 저장합니다
feature_names = preprocessor.get_feature_names_out()
processed_df = pd.DataFrame(new_processed, columns=feature_names)
export_df = pd.concat([new_members[["member_id"]].reset_index(drop=True), processed_df], axis=1)
output_path = OUTPUT_DIR / "week1_new_members_processed.csv"
export_df.to_csv(output_path, index=False)
assert export_df.shape == (100, 68)
assert export_df.isna().sum().sum() == 0
print(output_path, export_df.shape)


print("[PASS] 1주차 8교시 전체 실행 완료")
