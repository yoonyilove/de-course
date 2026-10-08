"""2주차 3교시 전체 실행본: 표 모양 변환과 저장."""

from pathlib import Path
import pandas as pd
from IPython.display import display

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


# Q1. 4명과 7일만 골라 표 모양을 눈으로 확인할 준비를 합니다
member_ids = ["M001", "M002", "M003", "M004"]
dates = sorted(activity["activity_date"].unique())[:7]
small = activity.query("member_id in @member_ids and activity_date in @dates")
print(small.shape)


# Q2. 회원은 행에 두고 날짜를 열로 펼쳐 비교합니다
wide = small.pivot_table(
    index="member_id", columns="activity_date",
    values="app_opens", aggfunc="sum", fill_value=0
)
print(wide.shape)
display(wide)


# Q3. 날짜 열 7개를 다시 한 개의 날짜 열로 모읍니다
long_again = wide.reset_index().melt(
    id_vars="member_id",
    var_name="activity_date",
    value_name="app_opens"
)
print(long_again.shape)


# Q4. 체류 시간을 숫자로 정리하고 CSV와 Parquet로 저장합니다
activity_export = activity.copy()
activity_export["stay_time_min"] = pd.to_numeric(activity_export["stay_time_min"], errors="coerce")
csv_path = OUTPUT_DIR / "activity_merged.csv"
parquet_path = OUTPUT_DIR / "activity_merged.parquet"
activity_export.to_csv(csv_path, index=False)
activity_export.to_parquet(parquet_path, index=False)
print(csv_path.exists(), parquet_path.exists())


# Q5. 저장한 파일을 다시 읽어 크기와 자료형을 확인합니다
csv_back = pd.read_csv(csv_path)
parquet_back = pd.read_parquet(parquet_path)
assert csv_back.shape == activity_export.shape
assert parquet_back.shape == activity_export.shape
print(csv_back.shape, parquet_back.shape)


print("[PASS] 2주차 3교시 전체 실행 완료")
