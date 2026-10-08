"""2주차 2교시 전체 실행본: 출처 병합."""

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


# Q1. 첫 CSV를 열어 1,200행×9열인지 확인합니다
batch_files = sorted((DATA_DIR / "activity_batches").glob("activity_batch_*.csv"))
first_batch = pd.read_csv(batch_files[0])
print(first_batch.shape)
print(first_batch.columns.tolist())


# Q2. 파일을 읽을 때 출처 파일명을 한 열로 붙입니다
frames = []
for file_path in batch_files[:3]:
    one_batch = pd.read_csv(file_path)
    one_batch["source_file"] = file_path.name
    frames.append(one_batch)
print(len(frames), frames[0].shape)


# Q3. concat은 DataFrame 세 개를 아래로 이어 붙입니다
sample_activity = pd.concat(frames, ignore_index=True)
print(sample_activity.shape)
print(sample_activity.index[[0, -1]].tolist())


# Q4. 같은 코드를 25개 전체로 확장합니다
frames = []
for file_path in batch_files:
    one_batch = pd.read_csv(file_path)
    one_batch["source_file"] = file_path.name
    frames.append(one_batch)
activity = pd.concat(frames, ignore_index=True)
print(activity.shape, activity["source_file"].nunique())


# Q5. 원본의 전체 행 수와 합친 표의 행 수를 비교합니다
source_rows = sum(len(pd.read_csv(p)) for p in batch_files)
assert len(activity) == source_rows
assert activity["source_file"].nunique() == 25
print(source_rows, len(activity))


print("[PASS] 2주차 2교시 전체 실행 완료")
