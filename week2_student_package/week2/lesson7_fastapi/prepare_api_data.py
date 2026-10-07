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
WEEK2_DIR = DATA_DIR.parents[1] / "week2"
OUTPUT_DIR = WEEK2_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
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

summary_path = OUTPUT_DIR / "member_activity_summary.csv"
model_table.to_csv(summary_path, index=False)
print("저장:", summary_path)
print("크기:", model_table.shape)
