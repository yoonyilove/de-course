"""2주차 6교시 전체 실행본: 파이프라인 저장."""

from pathlib import Path
import numpy as np
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
ARTIFACT_DIR = WEEK2_DIR / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)
print("데이터 폴더:", DATA_DIR)
batch_files = sorted((DATA_DIR / "activity_batches").glob("activity_batch_*.csv"))
frames = []
for file_path in batch_files:
    one_batch = pd.read_csv(file_path)
    one_batch["source_file"] = file_path.name
    frames.append(one_batch)
activity = pd.concat(frames, ignore_index=True)

activity["activity_dt"] = pd.to_datetime(activity["activity_date"], errors="coerce")
activity["stay_time_min_num"] = pd.to_numeric(activity["stay_time_min"], errors="coerce")
activity["active_dt"] = activity["activity_dt"].where(activity["logged_in"])

member_activity = activity.groupby("member_id").agg(
    active_days=("logged_in", "sum"),
    total_app_opens=("app_opens", "sum"),
    total_stay_time_min=("stay_time_min_num", "sum"),
    total_profile_views=("profile_views", "sum"),
    total_recommendations_viewed=("recommendations_viewed", "sum"),
    total_messages_sent=("messages_sent", "sum"),
    avg_reply_delay_sec=("avg_reply_delay_sec", "mean"),
    last_active_date=("active_dt", "max"),
).reset_index()
reference_date = pd.Timestamp("2026-07-01")
member_activity["days_since_last_activity"] = (
    reference_date - member_activity["last_active_date"]
).dt.days

members = pd.read_csv(DATA_DIR / "members.csv")
member_columns = [
    "member_id", "gender", "age", "residence_region",
    "membership_tier", "signup_channel", "meeting_scheduled"
]
model_table = members[member_columns].merge(
    member_activity, on="member_id", how="left", validate="one_to_one"
)

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

numeric_features = [
    "age", "active_days", "total_app_opens", "total_stay_time_min",
    "total_profile_views", "total_recommendations_viewed",
    "total_messages_sent", "avg_reply_delay_sec", "days_since_last_activity"
]
categorical_features = [
    "gender", "residence_region", "membership_tier", "signup_channel"
]
X = model_table[numeric_features + categorical_features]
y = model_table["meeting_scheduled"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
numeric_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])
categorical_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])
preprocessor = ColumnTransformer([
    ("num", numeric_pipe, numeric_features),
    ("cat", categorical_pipe, categorical_features),
], verbose_feature_names_out=False).set_output(transform="pandas")
import joblib


# Q1. train 800명으로 빈값 대체값과 변환 기준을 배웁니다
train_processed = preprocessor.fit_transform(X_train)
print(train_processed.shape)
print(type(train_processed))


# Q2. test 200명에는 train에서 배운 기준만 적용합니다
test_processed = preprocessor.transform(X_test)
print(test_processed.shape)
print(train_processed.columns.equals(test_processed.columns))


# Q3. 변환한 두 표의 크기와 남은 빈값을 검사합니다
missing_train = train_processed.isna().sum().sum()
missing_test = test_processed.isna().sum().sum()
assert train_processed.shape == (800, 36)
assert test_processed.shape == (200, 36)
print(missing_train, missing_test)


# Q4. 학습이 끝난 전처리기를 joblib 파일로 저장합니다
artifact_path = ARTIFACT_DIR / "matchmaking_preprocessor.joblib"
joblib.dump(preprocessor, artifact_path)
print(artifact_path.exists(), artifact_path.stat().st_size)


# Q5. 저장한 전처리기를 다시 불러와 같은 결과인지 비교합니다
loaded_preprocessor = joblib.load(artifact_path)
test_again = loaded_preprocessor.transform(X_test)
same = np.allclose(test_processed.to_numpy(), test_again.to_numpy())
assert same
print(test_again.shape, same)


print("[PASS] 2주차 6교시 전체 실행 완료")
