"""3주차 1교시 · API에서 회원 데이터를 받아 원본 CSV로 남기기.

먼저 course_materials 폴더의 별도 터미널에서 서버를 실행합니다.

그다음 이 파일을 실행합니다. API 서버가 꺼져 있으면 Q1에서 연결 오류가 납니다.
"""

# 파일과 폴더 주소를 다루기위해 Path 클래스도구를 Pathlib 라이브러리모듈에서 가져옵니다. 
from pathlib import Path

# Python이 다른 .py 파일의 경로를 찾는 목록을 사용하기 위해 필요한 sys모듈을 가져옵니다. 
# sys모듈은 파이썬 인터프리터의 동작을 제어하고 환경 변수를 관리하는 데 사용됩니다.
import sys

# 현재 .py 파일의 실제 위치를 Path 객체로 만듭니다.
# __file__ 은 파일의 절대경로를 나타내는 내장변수이며, resolve() 메서드는 경로를 정규화하여 사용할 수 있게 합니다.
HERE = Path(__file__).resolve()

# 경로객체에 기본내장인 parents 메서드를 사용하여, 이 파일의 폴더에서 두 단계 위에 있는 week3 폴더를 가리킵니다.
WEEK3_DIR = HERE.parents[1]

# week3_common.py를 불러올 수 있도록 week3 폴더를 검색 경로에 추가합니다.
# sys.path는 파이썬 인터프리터가 찾을 수 있는 모듈 경로 목록을 저장하는 리스트입니다.
# append는 맨 뒤에 덧붙여서 탐색 후순위가 되지만, insert(0, ...)는 맨 앞에 끼워 넣어 내 프로젝트 폴더를 탐색 1순위로 만듭니다.
if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))

# CSV 파일을 DataFrame으로 읽고 저장하는데 필요한 Pandas 라이브러리를 가져옵니다.
import pandas as pd

# 실행 중인 API 서버에 HTTP 요청을 보내고 응답을 받는 requests 라이브러리를 가져옵니다.
import requests

# 받은 시각을 파일 이름에 넣을 때 사용하는 Python 표준 라이브러리 datetime을 가져옵니다.
from datetime import datetime

# 공통 파일에서 제공 데이터 폴더와 API 원본 저장 폴더를 가져옵니다.
from week3_common import DATA_DIR, RAW_DIR

# 서버를 실행할 때 지정한 주소와 같은 API 기본 주소를 문자열로 저장합니다.
# 127.0.0.1은 현재 컴퓨터를 가리키고, 8000은 서버가 요청을 기다리는 포트 번호입니다.
# 뒤에서 "/health"나 "/members"를 이어 붙여 실제 요청 주소를 만듭니다.
API_URL = "http://127.0.0.1:8000"

# API 서버에 연결할 수 없을 때 비교용으로 사용할 수 있는 수업 제공 CSV입니다.
# 이 파일을 자동으로 API 자료로 바꾸는 것은 아니며, 서버 문제를 확인할 때 참고하는 대체 입력입니다.
# 프로젝트 기준 위치: course_materials/matchmaking_data/03_week3/api_members_fallback.csv
fallback_path = DATA_DIR / "api_members_fallback.csv"

# API에서 받은 원본 CSV를 넣을 폴더가 없다면 만듭니다. 파일 저장은 아직 하지 않습니다.
# RAW_DIR은 API에서 받은 가공 전 원본 CSV를 모아 둘 위치를 한 번 정해 두기 위해 만든 것입니다.
# mkdir(parents=True, exist_ok=True)는 상위 폴더까지 필요하면 만들고,
# 폴더가 이미 있으면 오류 없이 그대로 사용합니다.
RAW_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------
# Q1. API 서버가 실행 중인지 확인하는 상태 확인 요청을 보냅니다.
# ------------------------------

# API_URL과 "/health" 문자열을 +로 이어
# http://127.0.0.1:8000/health라는 GET 요청 주소를 만듭니다.
# timeout=5는 서버가 응답하지 않을 때 최대 5초만 기다리고 오류를 내라는 설정입니다.
# health_response에는 requests.get()이 돌려준 requests.Response라는 응답객체가 들어갑니다. 
# 이 객체 안에는 상태코드(예:200)와 응답내용(직접작성해둔)이 담여있습니다. 
# 상태코드는 속성입니다. ()를 쓰지 않는 것도 이에 기인합니다.  
# 응답객체.json()은 메소드로서, json 본문을 python 값으로 변환합니다. 
health_response = requests.get(API_URL + "/health", timeout=5)

# 응답 객체의 status_code에는 HTTP 상태 코드가 들어 있습니다. 보통 200이면 정상 응답입니다.
print("서버 상태 코드:", health_response.status_code)

# json()은 서버 응답 본문의 JSON을 Python dict나 list로 읽어 주는 메서드입니다.
# /health 주소를 요청했기 때문에 여러 회원 목록이 아니라 JSON 객체 하나가 옵니다.
# /members처럼 서버가 여러 회원을 보내면 JSON 배열이므로 Python list가 됩니다.
print("서버 응답 내용:", health_response.json())


# ------------------------------
# Q2. /members 주소에 회원 자료를 요청합니다.
# ------------------------------

# members_response에는 requests.get()이 돌려준 requests.Response라는 응답객체가 들어갑니다. 
# API_URL과 "/members" 문자열을 +로 이어
# http://127.0.0.1:8000/members라는 GET 요청 주소를 만듭니다.
# params는 서버에 함께 전달할 요청 조건입니다.
# params에 {"limit": 100}을 넣습니다. 최대 100명의 회원을 요청한다는 의미입니다. 
# requests가 이를 URL의 ?limit=100 조건으로 바꾸어 서버에 전달합니다.
# limit=100은 서버에 최대 100명의 회원을 달라고 요청하는 조건입니다.
# timeout=5는 서버가 응답하지 않을 때 최대 5초만 기다리고 오류를 내라는 설정입니다.
members_response = requests.get(
    API_URL + "/members", params={"limit": 100}, timeout=5
)

# 400번대나 500번대처럼 문제가 있는 응답이면 여기서 예외를 발생시킵니다.
# 정상 응답이면 아무것도 반환하지 않고 다음 줄로 진행합니다.
members_response.raise_for_status()

# 응답객체 members_response의 메소드 json()은 응답 본문의 JSON을 Python 값으로 바꾸어 반환합니다.
# payload라는 변수명에 반환값을 저장합니다. 영어로는 “운반되는 내용물”이라는 뜻입니다. 
# API에서는 서버가 보내거나 받는 실제 데이터 내용물을 payload라고 부르는 경우가 많습니다.
#
# 이 서버의 /members 응답은 회원 한 명을 나타내는 dict 100개가 들어 있는 list입니다.
# payload는 아직 DataFrame이 아니라 서버가 보낸 원래 Python 자료 (여기서는 list)를 담아두게 됩니다. 
payload = members_response.json()

# type()으로 자료형을 확인하고 len()으로 list 안의 회원 수를 확인합니다.
print("받은 자료형과 회원 수:", type(payload), len(payload))


# ------------------------------
# Q3. list 안의 회원 dict들을 행과 열이 있는 DataFrame으로 바꿉니다.
# ------------------------------

# payload에 받은 list를 dataframe표로 바꾼 후 raw_members 변수에 담습니다. 
# dict의 key는 열 이름이 되고, 각 dict의 value는 한 행의 값이 됩니다.
# 이렇게 바꾸면 shape, columns, to_csv 같은 Pandas 기능을 사용할 수 있습니다.
raw_members = pd.DataFrame(payload)

# 조금 전 만든 raw_members Dataframe표의 회원 수(행 ___수)와 열 수를 함께 확인합니다.
# shape은 표의 모양을 속성으로 저장해두며, tuple 형태로 (행 수, 열 수)를 반환합니다. 
print("회원표 크기:", raw_members.shape)

# raw_members의 dataframe의 열 이름을 표시해보겠습니다. 
# DataFrame의 columns 속성에는 현재 표의 모든 열 이름이 들어 있습니다.
# columns는 메서드가 아니라 열 이름을 꺼내는 속성이므로 괄호를 쓰지 않습니다.
# columns의 결과는 Pandas의 Index 객체입니다.
# Index 객체의 tolist() 메서드를 사용하면
# 열 이름을 일반 Python list로 바꿀 수 있습니다.
print("열 이름:", raw_members.columns.tolist())


# ------------------------------
# Q4. API에서 받은 원본표를 파일로 저장합니다.
# ------------------------------

# datetime은 Python 표준 라이브러리 datetime에서 가져온 날짜·시간 클래스입니다.
# datetime.now()는 이 클래스를 사용해 현재 날짜와 시각을 datetime 객체로 만듭니다.
# 그 뒤의 strftime()은 방금 만들어진 datetime 객체에 적용하는 메서드입니다.
# string format time의 줄임말이며, 날짜·시간을 지정한 문자열 형식으로 바꿉니다.
# strftime()은 날짜·시간을 20261012_153000 같은 파일 이름용 문자열로 바꿉니다.
# %Y  → 네 자리 연도, %m  → 두 자리 월, %d  → 두 자리 일
# %H  → 시, %M  → 분, %S  → 초, 중간의 _는 파일 이름에서 날짜와 시각을 구분하기 위한 일반 문자입니다.
# 최종 결과는 예를 들어 "20261012_153000" 같은 문자열이 됩니다.
# 이 문자열을 collected_at이라는 변수에 저장합니다.
collected_at = datetime.now().strftime("%Y%m%d_%H%M%S")

# f-string 안의 {collected_at} 자리에 받은 시각 문자열을 넣어 파일 이름을 만듭니다.
# / 연산자는 RAW_DIR Path와 파일 이름을 이어 새 Path 객체를 만듭니다. 
# RAW_DIR은 week3_common에서 가져온 경로객체 변수로, API에서 받은 가공 전 원본 CSV를 모아 둘 위치입니다. 
# 즉, raw_path는 저장할 파일의 위치를 나타내는 Path 객체입니다. 
raw_path = RAW_DIR / f"raw_{collected_at}.csv"

# raw_members DataFrame을 위에서 정한 파일명의 CSV 파일로 저장합니다.
# index=False는 Pandas의 0, 1, 2… 행 번호를 별도 CSV 열로 저장하지 않도록 하는 설정입니다. 
raw_members.to_csv(raw_path, index=False)

# 저장에 사용한 실제 경로를 출력합니다.
print("저장한 파일:", raw_path)

# Path.exists()는 그 위치에 파일이 실제로 생겼는지 True·False로 확인합니다.
print("파일 존재 여부:", raw_path.exists())


# ------------------------------
# Q5. 방금 저장한 CSV를 다시 읽어 실제로 사용할 수 있는지 확인합니다.
# ------------------------------
# 저장 명령이 끝났다는 사실만 믿지 않고, 같은 파일을 다시 읽는 기본 검증입니다.
# 저장한 API 원본 CSV를 다시 읽어 DataFrame으로 만듭니다.
# raw_path는 저장된 파일의 위치를 담은 Path 객체입니다.
# raw_back은 저장 후 다시 읽은 표라는 뜻의 변수 이름입니다.
raw_back = pd.read_csv(raw_path)

# 수업용 대체 CSV도 별도의 DataFrame으로 읽습니다.
# fallback_path는 대체 CSV의 위치이고,
# fallback_members는 그 파일을 읽은 표입니다.
# 원본표를 덮어쓰지 않고 별도로 보관합니다.
fallback_members = pd.read_csv(fallback_path)

# 다시 읽은 표의 행·열 수가 원래 표와 같은지 shape 속성을 이용해 확인합니다. 
# 모양이 다르면 assert에서 오류가 나고, 파일 저장·읽기 과정부터 점검해야 합니다.
assert raw_back.shape == raw_members.shape

# 다시 읽은 API 표와 대체 표의 크기를 shape으로 함께 출력해 비교합니다.
# 다시 읽은 표는 raw_back, 대체csv 읽은 표는 fallback_members 입니다. 
print("다시 읽은 표 / 대체 표:", raw_back.shape, fallback_members.shape)
print("[PASS] 3주차 1교시 완료")
