"""3주차 2교시 · Streamlit 기초를 한 줄씩 읽는 완성 예제

API 또는 CSV의 회원 데이터를 브라우저에 보여 주는 예제입니다.
"""

from pathlib import Path
import sys

HERE = Path(__file__).resolve()

WEEK3_DIR = HERE.parents[1]
if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))

import pandas as pd
import requests

# Python 코드의 실행 결과를 버튼·문장·표 같은 브라우저 화면 요소로 바꾸는 Streamlit을 가져옵니다.
# 긴 모듈 이름 대신 코드에서 st라는 짧은 별칭을 쓰기위해 as를 씁니다. 
import streamlit as st

# 3주차 공통 파일(week3_common.py)에 미리 정해 둔 데이터 폴더 경로 DATA_DIR를 가져옵니다.
# DATA_DIR은 폴더 위치를 담은 Path 객체이고, 아래에서 대체 CSV의 주소를 만들 때 사용합니다.
from week3_common import DATA_DIR


# 3주차 실습에서 사용할 수업용 API 서버의 기본 주소를 문자열로 저장합니다.
# 화면의 "API에서 회원 100명 받기" 버튼을 누르면
# API_URL 뒤에 "/members"를 붙여 회원 목록을 요청하게 될 때, 쓰이는 변수입니다. 
API_URL = "http://127.0.0.1:8000"

# api_members_fallback.csv를 읽어들여할 때 필요한 객체를 미리 만들어둡니다.
# DATA_DIR은 Path 객체이므로 / 연산자로 폴더와 파일 이름을 이어 새 Path 객체를 만듭니다.
# 이 줄은 파일을 읽거나 만들지 않고, 파일 주소만 fallback_path에 저장합니다.
fallback_path = DATA_DIR / "api_members_fallback.csv"


# 브라우저 앱의 기본 화면 설정을 정합니다.
# st.set_page_config()는 Streamlit 화면의 기본 설정을 정하는 함수입니다.
# page_title은 이 함수가 미리 정해 둔 설정 이름입니다.
#
# 함수 호출에서 page_title="회원 활동 데이터 확인"처럼
# 설정 이름과 값을 =로 연결하면
# page_title 설정에 오른쪽 값을 넣겠다는 뜻입니다.
#
# "회원 활동 데이터 확인"은 화면에 표시할 글자이므로
# 문자열이라는 것을 나타내기 위해 큰따옴표로 감쌉니다.
# 따옴표가 없으면 Python은 이를 변수 이름으로 해석합니다.
#
# 이 문자열은 브라우저 탭에 제목으로 표시됩니다.
# layout="wide"도 layout 설정에 "wide"라는 문자열 값을 넣는 문법입니다.
# wide는 화면을 넓게 사용하라는 Streamlit의 미리 정해진 설정값입니다.
st.set_page_config(
    page_title="회원 활동 데이터 확인",
    layout="wide",
)

# st.title()은 브라우저 화면에 가장 큰 제목을 표시하는 Streamlit 함수입니다.
# 따옴표 안의 문자열이 화면에 그대로 제목으로 나타납니다.
# "회원 활동 데이터 확인"를 제목으로 나타나게 해봅시다. 
st.title("회원 활동 데이터 확인")

# st.write()는 문자열·숫자·DataFrame 등 여러 Python 값을 브라우저에 표시합니다.
# 여기서는 사용자가 이 앱에서 할 일을 한 문장으로 안내합니다.
# "API 또는 CSV에서 회원 데이터를 불러와 화면에 표시합니다."를 나타나게 해봅시다. 
st.write("API 또는 CSV에서 회원 데이터를 불러와 화면에 표시합니다.")


# ------------------------------
# Q1. 대체 CSV를 읽을 준비를 합니다.
# ------------------------------

# 학생이 버튼을 누르거나 파일을 올리기 전에도 화면에 표가 보이도록
# 수업에서 제공한 fallback_path의 CSV를 먼저 읽습니다.
# pd.read_csv()는 CSV 파일을 읽어 DataFrame으로 반환하고,
# 그 결과를 raw_members라는 현재 화면용 원본표 변수에 저장합니다.
raw_members = pd.read_csv(fallback_path)

# 화면에 현재 표가 어디에서 왔는지 보여 주기 위한 문자열 변수입니다.
# API나 업로드 파일을 사용하면 아래에서 이 값을 새 문자열로 바꿉니다.
input_source = "제공된 대체 CSV"


# ------------------------------
# Q2. 버튼을 누르면 API에서 회원 데이터를 받습니다.
# ------------------------------

# st.button()은 브라우저에 버튼을 만들고,
# 이번 실행에서 사용자가 버튼을 눌렀으면 True, 누르지 않았으면 False를 반환합니다.
# 반환된 Boolean 값을 clicked라는 변수에 저장합니다.
clicked = st.button("API에서 회원 100명 받기")

# if clicked:는 clicked가 True일 때만 아래 들여쓴 코드를 실행하라는 뜻입니다.
# 버튼을 누르지 않은 실행에서는 API 요청을 보내지 않고 기본 CSV를 그대로 사용합니다.
if clicked:
    try:
        # requests.get()으로 API의 /members 주소에 GET 요청을 보냅니다.
        # params={"limit": 100}은 URL 뒤에 ?limit=100 조건을 붙여 최대 100명을 요청합니다.
        # timeout=5는 서버가 응답하지 않을 때 최대 5초까지만 기다리게 합니다.
        response = requests.get(
            API_URL + "/members",
            params={"limit": 100},
            timeout=5,
        )

        # 응답 객체의 상태 코드를 확인합니다.
        # 정상 응답이면 다음 줄로 진행하고, 400번대·500번대이면 HTTPError를 발생시킵니다.
        response.raise_for_status()

        # response.json()은 서버가 보낸 JSON 배열을 Python list로 바꿉니다.
        # 배열 안에는 회원 한 명씩을 나타내는 dict가 들어 있습니다.
        # pd.DataFrame()은 list[dict]를 행·열이 있는 표로 바꿉니다.
        # API에서 받은 표로 raw_members를 새로 가리키게 합니다.
        raw_members = pd.DataFrame(response.json())

        # 현재 입력 출처를 화면에 표시할 문장으로 바꿉니다.
        # 현재 입력 출처는 "API 응답"입니다. 
        # 화면에 현재 표가 어디에서 왔는지 보여 주기 위한 문자열 변수는 input_source 였습니다. 
        input_source = "API 응답"

        # st.success()는 성공을 알리는 초록색 안내 상자를 브라우저에 표시합니다.
        # API 요청과 DataFrame 변환이 오류 없이 끝난 뒤, 사용자가 누른 작업이 완료되었다는 것을 알려주기 위함입니다. 
        st.success("API에서 회원 데이터를 받았습니다.")

    # try 안에서 API 요청 중 오류가 발생하면 except 블록으로 이동합니다.
    # 예를 들어 서버가 꺼져 있거나, 주소가 틀렸거나,
    # 5초 안에 응답하지 않으면 오류가 발생할 수 있습니다.
    #
    # requests.RequestException은 requests에서 발생하는
    # 연결·시간 초과·HTTP 요청 관련 오류를 뜻합니다.
    # as error는 실제 발생한 오류 내용을 error라는 변수에 저장합니다.
    except requests.RequestException as error:

        # error 변수에는 오류의 종류와 원인이 들어 있습니다.
        # f-string의 {error} 위치에 그 오류 내용을 넣습니다.
        #
        # st.error()는 오류 안내 상자를 브라우저에 표시합니다.
        # API 요청은 실패했지만, 앞에서 먼저 읽어 둔 대체 CSV를
        # raw_members가 계속 가리키므로 화면은 계속 표시할 수 있습니다.
        st.error(f"API 요청에 실패했습니다. 대체 CSV를 계속 사용합니다: {error}")


# ------------------------------
# Q3. 사용자가 직접 CSV를 올릴 수 있게 합니다.
# ------------------------------

# st.file_uploader()는 브라우저에 파일 선택 UI를 만들고,
# 사용자가 선택한 파일을 업로드 파일 객체로 반환합니다.
# 파일 객체는 파일 자체를 Python이 다룰 수 있도록 감싸 놓은 객체입니다.
# 우리가 저장할 파일 객체의 이름은 uploaded_file 입니다
# uploaded_file에 표가 들어 있는 것이 아니라, 다음 정보를 가진 객체가 들어갑니다. (파일 이름, 파일 내용, 파일을 읽는 위치, 파일을 읽는 기능)
# type="csv"는 CSV 파일만 선택할 수 있게 제한합니다.
uploaded_file = st.file_uploader(
    "대체 CSV 선택",
    type="csv",
)

# 파일을 아직 고르지 않으면 uploaded_file은 None입니다.
# 파일을 실제로 골랐을 때만 uploaded_file is not None이 True가 되어 아래를 실행합니다.
if uploaded_file is not None:
    # 업로드 파일 객체를 pd.read_csv()에 넣어 DataFrame으로 읽습니다.
    # pd.read_csv()는 경로뿐 아니라 파일 객체도 받을 수 있습니다.
    # 기존 raw_members에 새 DataFrame을 다시 대입하므로 이후 화면은 업로드 표를 사용합니다.
    raw_members = pd.read_csv(uploaded_file)

    # 업로드 파일 객체의 name 속성에서 원래 파일 이름을 가져옵니다.
    # f-string으로 파일 이름을 안내 문장에 넣습니다.
    # 화면에 현재 표가 어디에서 왔는지 보여 주기 위한 문자열 변수는 input_source 였습니다. 
    input_source = f"업로드 파일: {uploaded_file.name}"

    # 업로드가 완료되었다는 성공 안내를 success를 활용해 브라우저에 표시합니다.
    st.success(f"{uploaded_file.name}을 읽었습니다.")


# ------------------------------
# Q4. 현재 데이터의 크기와 자료구조를 확인합니다.
# ------------------------------

# st.write()로 현재 회원표가 API·대체 CSV·업로드 파일 중 어디에서 왔는지 표시합니다.
st.write("현재 입력:", input_source)

# type(raw_members)는 현재 객체의 자료형을 알려 줍니다.
# __name__은 <class 'pandas.core.frame.DataFrame'>처럼 긴 경로 대신
# 자료형의 이름인 "DataFrame"만 꺼내는 속성입니다.
st.write("자료구조:", type(raw_members).__name__)

# DataFrame의 shape 속성은 (행 수, 열 수) tuple입니다.
# 괄호를 쓰지 않으므로 메서드가 아니라 표의 모양을 저장한 속성입니다.
st.write("표 크기:", raw_members.shape)

# head(10)은 DataFrame의 앞에서부터 10행을 골라 새 표를 반환합니다.
# st.dataframe()은 그 표를 브라우저에서 스크롤할 수 있는 표로 표시합니다.
st.dataframe(raw_members.head(10))


# ------------------------------
# Q5. 오늘 결과를 간단히 확인합니다.
# ------------------------------

# st.metric()은 화면에 핵심 숫자를 카드 형태로 표시하는 Streamlit 함수입니다.
# 즉, metric은 Streamlit 화면에서 중요한 숫자 하나를 크게 보여 줄 때 사용합니다.
# st.metric()은 보통 다음 순서로 값을 받습니다: st.metric(label, value)
# Python은 첫 번째 값을 label(지표의 이름)), 두 번째 값을 value(화면에 크게 표시할 숫자나 값)으로 해석합니다.

# shape[0]은 (행 수, 열 수) 중 첫 번째 값이므로 회원 수를 뜻합니다.
st.metric("회원 수", raw_members.shape[0])

# shape[1]은 두 번째 값이므로 현재 표의 열 수를 뜻합니다.
st.metric("열 수", raw_members.shape[1])

# st.success()로 현재 표를 브라우저에 표시했다는 완료 안내를 보여 줍니다.
st.success("회원 데이터를 브라우저 화면에 표시했습니다.")
