"""3주차 수업용 로컬 API.

Uvicorn이 이 파일을 불러올 때 api_members_fallback.csv의 회원 100명×16열을
DataFrame으로 읽어 메모리에 준비한다. /health는 준비된 행 수를 확인하고,
/members는 그 DataFrame의 회원 행을 JSON으로 돌려준다.
"""

# 파일과 폴더 주소를 다루기 위해 Path 클래스를 가져옵니다.
from pathlib import Path

# CSV를 DataFrame으로 읽고, 행을 고르고, JSON으로 바꾸기 전에 결측치를 처리하는 데 사용합니다.
import pandas as pd

# FastAPI는 API 서버 객체를 만들고, Query는 URL 요청값의 기본값과 허용 범위를 정합니다.
from fastapi import FastAPI, Query


# 현재 support_api.py 파일의 실제 위치를 Path 객체로 만듭니다.
# __file__은 현재 실행 중인 .py 파일의 경로이고,
# resolve()는 상대 경로를 절대 경로로 정리합니다.
# parent는 파일 이름을 제외하고 support_api.py가 들어 있는 week3 폴더를 가리킵니다.
HERE = Path(__file__).resolve().parent

# API가 읽을 CSV 파일의 위치를 만듭니다.
# HERE.parent는 week3 폴더의 상위인 course_materials 폴더입니다.
# 그 아래 matchmaking_data/03_week3/api_members_fallback.csv를 이어 붙입니다.
# 이 줄은 아직 파일을 읽지 않고, 파일 주소를 DATA_PATH에 저장합니다.
DATA_PATH = HERE.parent / "matchmaking_data" / "03_week3" / "api_members_fallback.csv"

# 서버가 시작될 때 CSV 파일을 읽어 DataFrame으로 메모리에 올립니다.
# Uvicorn이 support_api.py를 불러오면 이 줄도 위에서부터 실행됩니다.
# 따라서 API가 응답하려면 이 CSV가 DATA_PATH에 실제로 있어야 합니다.
# summary는 회원 100명 × 16열의 원본 회원표를 담는 DataFrame입니다.
summary = pd.read_csv(DATA_PATH)

# FastAPI 서버 객체를 만듭니다.
# Uvicorn 명령의 support_api:app에서 콜론 뒤 app이 바로 이 객체를 가리킵니다.
# title은 자동 문서 화면(/docs)에 표시되는 API 이름입니다.
app = FastAPI(title="Week 3 Matchmaking Activity API")


@app.get("/health")
def health():
    # /health 주소로 GET 요청이 오면 이 함수가 실행됩니다.
    # status는 서버가 정상적으로 응답하고 있음을 나타내는 문자열입니다.
    # rows는 서버가 메모리에 준비해 둔 summary의 행 수를 알려 줍니다.
    # len(summary)는 회원 수를 세는 것이며, HTTP 상태 코드 200과는 다른 값입니다.
    return {"status": "ok", "rows": len(summary)}


@app.get("/members")
def get_members(limit: int = Query(100, ge=1, le=100)):
    # /members 주소로 GET 요청이 오면 이 함수가 실행됩니다.
    # limit은 URL에서 요청할 회원 수입니다. 예: /members?limit=3
    # Query(100, ge=1, le=100)는 기본값을 100으로 하고,
    # 1명부터 100명까지만 요청하도록 FastAPI가 검사하게 합니다.

    # head(limit)는 summary의 위에서부터 limit개 행을 골라 새 DataFrame을 만듭니다.
    # 원본 summary 전체를 바꾸는 것이 아니라, 응답에 사용할 일부 표를 rows에 담습니다.
    rows = summary.head(limit)

    # JSON에는 NumPy의 NaN을 그대로 보낼 수 없으므로 응답용 표를 정리합니다.
    # astype(object)는 숫자 열도 Python 객체를 담을 수 있는 자료형으로 바꿉니다.
    # pd.notna(rows)는 빈값이 아닌 칸을 True로 표시합니다.
    # where(..., None)은 값이 있으면 원래 값을 유지하고, 빈값이면 Python의 None으로 바꿉니다.
    safe_rows = rows.astype(object).where(pd.notna(rows), None)

    # DataFrame의 각 행을 하나의 dict로 바꾼 list를 반환합니다.
    # orient="records"는 한 행을 한 dict로 표현하라는 설정입니다.
    # FastAPI는 이 Python list[dict]를 JSON 응답으로 자동 변환합니다.
    return safe_rows.to_dict(orient="records")
