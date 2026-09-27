"""1주차 학생용 폴더의 파일과 기본 Python 환경을 확인합니다."""

from pathlib import Path
import importlib.util
import platform
import sys


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "matchmaking_data" / "01_week1"


def check_path(label: str, path: Path) -> bool:
    ok = path.exists()
    print(f"[{'PASS' if ok else 'FAIL'}] {label}: {path}")
    return ok


print("=== 1주차 학생용 환경 점검 ===")
print(f"[PASS] 운영체제: {platform.system()} {platform.release()}")
print(f"[PASS] Python 버전: {sys.version.split()[0]}")
print(f"[PASS] Python 위치: {sys.executable}")
print(f"[PASS] 학생용 폴더: {ROOT}")

required_paths = [
    ("1주차 데이터 폴더", DATA_DIR),
    ("회원 데이터", DATA_DIR / "matchmaking_members.csv"),
    ("선호조건 데이터", DATA_DIR / "matchmaking_preferences.csv"),
    ("새 회원 데이터", DATA_DIR / "matchmaking_members_new.csv"),
    ("1주차 1교시 노트북", ROOT / "week1" / "lesson1_list_type_flow" / "1주차_1교시_학생용_지적실험노트.ipynb"),
    ("1주차 8교시 노트북", ROOT / "week1" / "lesson8_capstone" / "1주차_8교시_학생용_지적실험노트.ipynb"),
    ("데이터 설명 슬라이드", DATA_DIR / "1주차_데이터_열이름과뜻_안내슬라이드.pptx"),
]

path_results = [check_path(label, path) for label, path in required_paths]

packages = {
    "numpy": "numpy",
    "pandas": "pandas",
    "scikit-learn": "sklearn",
    "JupyterLab": "jupyterlab",
    "IPython kernel": "ipykernel",
    "Matplotlib": "matplotlib",
    "Seaborn": "seaborn",
    "Requests": "requests",
    "Joblib": "joblib",
}
package_results = []
for label, module_name in packages.items():
    ok = importlib.util.find_spec(module_name) is not None
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    package_results.append(ok)

all_ok = all(path_results + package_results)
print()
if all_ok:
    print("모든 1주차 점검 항목이 PASS입니다. 첫 수업 노트북을 열어도 됩니다.")
else:
    print("FAIL 항목이 있습니다. setup 안내서와 오류 구조대를 먼저 확인하세요.")
    raise SystemExit(1)
