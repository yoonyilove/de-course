"""2주차 5교시 전체 실행본: 파이프라인 설계."""

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


# Q1. 계산할 숫자 열과 종류를 나타내는 문자 열을 나눕니다
numeric_features = ["age", "active_days", "total_app_opens", "total_stay_time_min", "total_profile_views", "total_recommendations_viewed", "total_messages_sent", "avg_reply_delay_sec", "days_since_last_activity"]
categorical_features = ["gender", "residence_region", "membership_tier", "signup_channel"]
print(len(numeric_features), len(categorical_features))


# Q2. 13개 입력 열 X와 일정 등록 여부 y를 따로 둡니다
X = model_table[numeric_features + categorical_features]
y = model_table["meeting_scheduled"]
print(X.shape, y.shape)


# Q3. 회원 1,000명을 train 800명과 test 200명으로 함께 나눕니다
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(X_train.shape, X_test.shape)


# Q4. 숫자 열은 빈값을 채운 뒤 크기 기준을 맞추도록 설계합니다
numeric_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
])
print(numeric_pipe.steps)


# Q5. 문자 열을 0·1 열로 바꾸고 숫자 처리와 한데 묶습니다
categorical_pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
])
preprocessor = ColumnTransformer([
    ("num", numeric_pipe, numeric_features),
    ("cat", categorical_pipe, categorical_features),
], verbose_feature_names_out=False).set_output(transform="pandas")
print(preprocessor)


print("[PASS] 2주차 5교시 전체 실행 완료")
