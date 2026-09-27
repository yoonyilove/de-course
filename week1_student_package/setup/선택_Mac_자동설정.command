#!/bin/zsh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COURSE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

CONDA_EXE=""
for candidate in /opt/miniconda3/bin/conda "$HOME/miniconda3/bin/conda" /opt/anaconda3/bin/conda "$HOME/anaconda3/bin/conda"; do
  if [ -x "$candidate" ]; then
    CONDA_EXE="$candidate"
    break
  fi
done

if [ -z "$CONDA_EXE" ]; then
  echo "[STOP] Miniconda를 찾지 못했습니다."
  echo "먼저 setup/01_MacBook_완전초보_설정.md의 2~4단계를 진행하세요."
  read "?Enter를 누르면 닫힙니다."
  exit 1
fi

CONDA_BASE="$($CONDA_EXE info --base)"
source "$CONDA_BASE/etc/profile.d/conda.sh"

echo "[1/4] de-course 환경을 만듭니다. 이미 있으면 그대로 사용합니다."
if ! conda env list | grep -q '^de-course '; then
  conda create -n de-course python=3.12 -y
fi

echo "[2/4] de-course 환경을 엽니다."
conda activate de-course

echo "[3/4] 3주 수업 패키지를 설치합니다. 시간이 걸릴 수 있습니다."
python -m pip install -r "$COURSE_ROOT/requirements.txt"

echo "[4/4] Jupyter 커널을 등록하고 상태를 확인합니다."
python -m ipykernel install --user --name de-course --display-name "Python (de-course)"
python "$COURSE_ROOT/setup/02_1주차_환경점검.py"

echo "완료되었습니다. 환경 점검 항목이 모두 PASS인지 확인하세요."
read "?Enter를 누르면 닫힙니다."
