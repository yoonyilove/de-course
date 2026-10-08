"""2주차 1교시 전체 실행본: 파일 찾기."""

from pathlib import Path

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


# Q1. 파일을 찾기 전에 데이터 폴더가 실제로 있는지 확인합니다
batch_dir = DATA_DIR / "activity_batches"
print(batch_dir)
print(batch_dir.exists())


# Q2. 같은 이름 규칙을 가진 CSV를 한꺼번에 찾습니다
found = list(batch_dir.glob("activity_batch_*.csv"))
print(type(found), len(found))


# Q3. 찾은 파일을 01번부터 25번까지 순서대로 놓습니다
batch_files = sorted(found)
print(batch_files[0].name)
print(batch_files[-1].name)


# Q4. 01번부터 25번까지 빠진 파일이 없는지 이름으로 확인합니다
expected_names = {f"activity_batch_{i:02d}.csv" for i in range(1, 26)}
actual_names = {p.name for p in batch_files}
missing = expected_names - actual_names
print(len(actual_names), missing)


# Q5. 잘못된 파일명 규칙을 고쳐 CSV 25개를 다시 찾습니다
wrong = sorted(batch_dir.glob("activity_*.txt"))
fixed = sorted(batch_dir.glob("activity_batch_*.csv"))
assert len(fixed) == 25
print(len(wrong), len(fixed))


print("[PASS] 2주차 1교시 전체 실행 완료")
