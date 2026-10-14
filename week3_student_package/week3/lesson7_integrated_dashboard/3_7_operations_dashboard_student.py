"""3주차 7교시 · 수집, 전처리, DB, 분석을 한 화면에 연결하기.

1~6교시에서 따로 만든 기능을 하나의 Streamlit 운영 화면에 연결합니다.
사용자는 화면에서 회원 데이터를 가져오고, 전처리하고, SQLite에 저장하고,
그래프와 PCA 결과를 확인할 수 있습니다.

이 파일은 다음 명령으로 실행합니다.
python -m streamlit run 3_7_operations_dashboard_explained.py

API 버튼을 사용하려면 1교시의 지원 API 서버도 별도 터미널에서 실행해야 합니다.
API를 사용하지 않을 때는 화면에서 CSV를 업로드하거나 제공된 대체 CSV를 선택할 수 있습니다.
"""


# 파일과 폴더 주소를 다루기 위해 pathlib 모듈의 Path 클래스를 가져옵니다.
# Path 객체를 사용하면 운영체제가 달라도 폴더와 파일 경로를 안전하게 이어 붙일 수 있습니다.
from pathlib import Path

# Python이 다른 .py 파일을 찾을 때 참고하는 모듈 검색 경로 목록을 다루기 위해 sys를 가져옵니다.
# 이 파일에서는 week3_common.py를 불러오기 전에 프로젝트의 week3 폴더를 검색 경로에 넣습니다.
import sys


# __file__은 현재 실행 중인 이 .py 파일의 위치를 담은 Python 내장 변수입니다.
# Path(__file__)은 문자열 경로를 Path 객체로 바꾸고,
# resolve()는 실제 절대 경로 형태로 정리합니다.
# HERE는 이후 경로 계산의 출발점이 되는 현재 파일의 위치입니다.
HERE = Path(__file__).resolve()

# HERE.parents[1]은 현재 파일의 폴더에서 두 단계 위에 있는 week3 폴더입니다.
# 3_7_operations_dashboard_explained.py가 lesson7_integrated_dashboard 안에 있으므로
# 첫 번째 상위 폴더는 lesson7_integrated_dashboard,
# 두 번째 상위 폴더는 week3가 됩니다.
WEEK3_DIR = HERE.parents[1]

# week3_common.py를 프로젝트의 week3 폴더에서 찾을 수 있도록 검색 경로를 준비합니다.
# sys.path는 Python이 import할 모듈을 찾는 폴더 경로들의 list입니다.
# 이미 들어 있지 않을 때만 insert(0, ...)으로 맨 앞에 추가합니다.
# 0은 탐색 우선순위가 가장 높은 위치라는 뜻입니다.
if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))


# 현재 시각을 collection_id로 만들 때 사용할 datetime 클래스를 가져옵니다.
from datetime import datetime

# CSV와 SQL 조회 결과를 DataFrame으로 읽고 다루기 위해 pandas를 pd라는 별칭으로 가져옵니다.
import pandas as pd

# API 서버에 HTTP 요청을 보내고 응답을 받기 위해 requests를 가져옵니다.
import requests

# 버튼, 안내 문장, 표, 그래프 같은 브라우저 화면 요소를 만들기 위해 streamlit을 st라는 별칭으로 가져옵니다.
import streamlit as st

# SQLite 데이터베이스 연결 객체를 만들고 테이블 목록을 확인하기 위해 SQLAlchemy 기능을 가져옵니다.
from sqlalchemy import create_engine, inspect

# 앞 교시에서 공통 파일에 미리 정의해 둔 값과 함수를 가져옵니다.
# 괄호 안에는 여러 이름을 한 번에 적을 수 있습니다.
# DATA_DIR와 DATABASE_DIR는 Path 객체이고,
# 나머지는 전처리·DB 저장·그래프·PCA 작업을 수행하는 함수입니다.
from week3_common import (
    DATA_DIR,
    DATABASE_DIR,
    load_preprocessor,
    transform_members,
    add_collection_columns,
    make_activity_figure,
    make_pca_result,
)


# 1교시 지원 API 서버의 기본 주소를 문자열로 저장합니다.
# 127.0.0.1은 현재 컴퓨터를 뜻하고, 8000은 API 서버가 요청을 기다리는 포트입니다.
# 실제 회원 목록을 요청할 때는 이 주소 뒤에 "/members"를 붙입니다.
API_URL = "http://127.0.0.1:8000"

# API 서버를 사용하지 못할 때 선택할 수 있는 수업용 대체 CSV의 위치입니다.
# DATA_DIR은 week3_common.py에서 가져온 3주차 데이터 폴더의 Path 객체입니다.
# 이 줄은 파일을 읽는 것이 아니라, 파일 주소를 fallback_path 변수에 저장합니다.
# fallback이라는 이름은 주 입력(API)이 어려울 때 사용할 보조 입력이라는 뜻입니다.
fallback_path = DATA_DIR / "api_members_fallback.csv"


# SQLite 파일을 저장할 폴더가 없으면 만듭니다.
# DATABASE_DIR는 데이터베이스 폴더를 가리키는 Path 객체입니다.
# parents=True는 필요한 상위 폴더도 함께 만들라는 뜻이고,
# exist_ok=True는 폴더가 이미 있어도 오류를 내지 말라는 뜻입니다.
# 폴더를 만드는 것과 DB 테이블을 만드는 것은 다른 작업입니다.
DATABASE_DIR.mkdir(parents=___, exist_ok=___)

# dashboard.db라는 SQLite 파일의 위치만 만듭니다.
# 아직 이 줄에서 테이블이나 데이터가 생성되는 것은 아닙니다.
db_path = DATABASE_DIR / "dashboard.db"

# create_engine()은 Python 코드가 SQLite 파일에 명령을 보낼 수 있게 하는
# SQLAlchemy 연결 객체를 만듭니다.
# f-string 안에 db_path를 넣어 sqlite:/// 형식의 SQLite 연결 주소를 만듭니다.
engine = create_engine(f"sqlite:///{db_path}")


def collect_members(api_url):
    """API에서 회원 최대 100명의 JSON을 받아 DataFrame으로 바꿉니다."""

    # 이 함수의 목표는 API 통신 과정을 한곳에 모아
    # 버튼 코드가 복잡해지지 않도록 하는 것입니다.
    # api_url은 API 기본 주소를 전달받는 매개변수입니다.
    # 함수 안에서만 사용할 입력 이름이므로, 호출할 때 API_URL 값을 전달합니다.

    # requests.get()은 서버에 GET 요청을 보내는 함수입니다.
    # api_url + "/members"는 회원 목록을 요청하는 주소입니다.
    # params는 URL에 붙일 조회 조건을 dict로 전달하는 설정입니다.
    # limit=100은 서버에 최대 100명의 회원을 요청한다는 뜻입니다.
    # timeout=5는 5초 안에 응답이 없으면 기다림을 끝내라는 설정입니다.
    response = requests.get(
        api_url + ___,
        params={"limit": ___},
        timeout=___,
    )

    # response는 requests.get()이 돌려준 응답 객체입니다.
    # raise_for_status()는 HTTP 상태 코드가 400번대나 500번대이면 예외를 발생시킵니다.
    # 정상 응답이면 아무것도 반환하지 않고 다음 줄로 진행합니다.
    response.___()

    # json()은 응답 본문의 JSON을 Python list와 dict로 변환합니다.
    # pd.DataFrame()은 그 list[dict]를 회원 한 명당 한 행인 DataFrame으로 바꿉니다.
    # return은 이 DataFrame을 함수 밖의 호출 위치로 돌려보냅니다.
    return pd.DataFrame(response.json())


def remember_raw(raw_members):
    """새 원본으로 바뀌면 이전 원본에 속한 처리 결과를 비웁니다."""

    # 이 함수의 목표는 화면이 다시 실행되어도 현재 원본표와
    # 그 원본으로 만든 처리표를 서로 섞지 않도록 관리하는 것입니다.
    # raw_members는 API나 CSV에서 새로 읽은 회원 원본 DataFrame입니다.

    # session_state는 같은 브라우저 세션에서 값을 보관하는 Streamlit 저장 공간입니다.
    # get("raw_members")는 해당 키의 값을 꺼내며,
    # 키가 아직 없으면 오류 대신 None을 반환합니다.
    previous = st.session_state.get("raw_members")

    # 처음 받은 자료이거나 이전 원본과 현재 원본의 내용이 다르면
    # 이전 원본으로 만든 processed_members를 삭제합니다.
    # DataFrame.equals()는 두 DataFrame의 모양과 값을 비교해 같은지 알려 줍니다.
    # not은 같지 않다는 뜻입니다.
    if previous is None or not previous.equals(raw_members):
        # pop()은 session_state에서 해당 키와 값을 삭제합니다.
        # 두 번째 인수 None은 키가 없어도 오류를 내지 않도록 하는 기본값입니다.
        st.session_state.pop("processed_members", None)

    # 현재 원본표를 session_state의 "raw_members"라는 키에 저장합니다.
    # Streamlit이 버튼 동작 뒤에 파일을 다시 실행해도
    # 같은 브라우저 세션에서 이 DataFrame을 다시 꺼낼 수 있습니다.
    st.session_state["raw_members"] = raw_members


def save_processed(processed_members, raw_members, engine):
    """처리된 행에 회원 ID·수집 ID를 붙여 SQLite에 추가합니다."""

    # 이 함수의 목표는 화면에서 만든 처리 결과를
    # 수집 시점 정보와 함께 SQLite 테이블에 저장하는 것입니다.
    # processed_members와 raw_members는 함수에 전달받는 DataFrame이고,
    # engine은 저장할 SQLite DB 연결 객체입니다.

    # datetime.now()로 현재 날짜와 시각을 가져옵니다.
    # strftime()으로 파일명·식별자에 사용할 문자열로 바꿉니다.
    # collection_id는 같은 시점에 함께 저장한 행들을 구분하는 우리가 만든 이름입니다.
    collection_id = datetime.now().strftime(___)

    # 처리표에 원본 회원 ID·수집 ID·원본 지역·회원권 등급을 붙입니다.
    # add_collection_columns()는 week3_common.py에 미리 정의된 공통 함수입니다.
    # 처리값과 식별 정보를 같은 행 순서로 맞춰 새로운 DataFrame을 반환합니다.
    rows = add_collection_columns(
        processed_members,
        raw_members,
        collection_id,
    )

    # rows DataFrame을 SQLite의 processed_members 테이블에 저장합니다.
    # if_exists="append"는 테이블이 있으면 기존 행을 지우지 않고 아래에 이어 쓰라는 뜻입니다.
    # 따라서 저장 버튼을 여러 번 누르면 같은 회원이 중복 저장될 수 있습니다.
    # index=False는 DataFrame의 행 번호를 별도 DB 열로 저장하지 않도록 합니다.
    rows.___(
        "processed_members",
        engine,
        if_exists=___,
        index=___,
    )


# 브라우저 화면에 이 대시보드의 가장 큰 제목을 표시합니다.
# st.title()은 Streamlit 화면에 제목을 표시하는 함수입니다.
st.title("회원 활동 데이터 운영 화면")


# ============================= Q1 =============================
# Q1의 목표는 사용자가 실제 작업 순서를 한 화면에서 이해하도록
# 데이터 가져오기·처리하기·저장 현황·분석 보기 구역을 만드는 것입니다.
# st.header()는 큰 제목보다 한 단계 작은 구역 제목을 표시합니다.
st.header("1. 데이터 가져오기")


# ============================= Q2 =============================
# Q2의 목표는 API나 CSV에서 원본 회원표를 가져오는 것입니다.
# Streamlit은 버튼이나 업로드 같은 동작이 일어날 때 .py 파일을 위에서부터 다시 실행합니다.
# 따라서 다음 버튼 실행에서도 사용할 원본표를 st.session_state에 보관해야 합니다.

# st.button()은 브라우저에 버튼을 만들고,
# 이번 실행에서 사용자가 눌렀으면 True, 누르지 않았으면 False를 반환합니다.
if st.___("API에서 회원 100명 받기"):
    # 버튼을 눌렀을 때만 들여쓴 API 요청 코드가 실행됩니다.
    try:
        # 1교시에서 만든 collect_members() 함수를 호출합니다.
        # API_URL을 전달하면 함수가 /members 요청을 보내고
        # 반환한 DataFrame을 raw_members 변수에 저장합니다.
        raw_members = collect_members(API_URL)

        # 현재 원본표를 세션에 저장합니다.
        # 이전 원본과 다르면 이전 처리 결과도 함께 지웁니다.
        remember_raw(raw_members)

        # st.success()는 성공했음을 알리는 색상 안내 상자를 브라우저에 표시합니다.
        # len(raw_members)는 DataFrame의 행 수, 즉 받은 회원 수입니다.
        st.success(f"{len(raw_members)}명을 받았습니다.")
    except requests.RequestException:
        # 서버가 꺼져 있거나 시간 초과·HTTP 오류가 발생하면 이 블록이 실행됩니다.
        # st.error()는 오류 상황을 브라우저에 표시합니다.
        st.error("API 서버를 확인하거나 아래에서 대체 CSV를 사용해 주세요.")


# 사용자가 자신의 컴퓨터에 있는 CSV를 선택할 수 있는 업로드 창을 만듭니다.
# st.file_uploader()는 파일을 선택하기 전에는 None을 반환하고,
# 파일을 선택하면 업로드 파일 객체를 반환합니다.
uploaded_file = st.___("대체 CSV 선택", type=___)
if uploaded_file is not None:
    # 파일을 선택했을 때만 실행됩니다.
    # 업로드 파일 객체를 pd.read_csv()에 전달하면 CSV 내용이 DataFrame이 됩니다.
    # API로 받은 표와 같은 raw_members 변수 흐름을 사용하도록 remember_raw()에 넘깁니다.
    remember_raw(pd.read_csv(uploaded_file))


# 화면에 파일을 직접 고르는 대신, 수업 폴더에 제공된 fallback CSV를 사용합니다.
# 버튼을 누른 경우에만 파일을 읽고, 그 결과를 현재 원본으로 세션에 저장합니다.
if st.___("제공된 대체 CSV 사용"):
    remember_raw(pd.read_csv(fallback_path))


# session_state 안에 "raw_members" 키가 있는지 확인합니다.
# in은 딕셔너리와 비슷한 저장 공간에서 키의 존재 여부를 검사합니다.
# has_raw는 원본표가 준비되었으면 True, 아직 없으면 False인 bool 변수입니다.
has_raw = "raw_members" in st.session_state
if has_raw:
    # 화면이 다시 실행되어도 session_state에 저장된 원본표를 꺼내
    # 현재 코드에서 사용할 raw_members라는 이름으로 연결합니다.
    raw_members = st.session_state["raw_members"]

    # st.metric()은 중요한 숫자를 카드 형태로 브라우저에 표시합니다.
    # 첫 번째 인수는 카드 제목, 두 번째 인수는 표시할 값입니다.
    # len(raw_members)는 DataFrame의 행 수, 즉 회원 수입니다.
    st.metric("원본 회원 수", len(raw_members))

    # head()는 원본 DataFrame을 바꾸지 않고 앞부분만 미리 보여 줄 표를 반환합니다.
    # st.dataframe()은 그 표를 브라우저에서 스크롤할 수 있는 표로 표시합니다.
    st.dataframe(raw_members.___())


# ============================= Q3 =============================
# Q3의 목표는 2주차에 저장한 전처리 규칙을
# 현재 원본표에 다시 적용하는 것입니다.
st.header("2. 처리하기")

# load_preprocessor()는 2주차에서 joblib 파일로 저장한 전처리기 객체를 읽어 반환합니다.
# 이 객체 안에는 결측치 처리 기준·숫자 스케일링 기준·문자 범주 목록이 들어 있습니다.
preprocessor = load_preprocessor()

# 원본표가 없으면 전처리할 입력이 없으므로 버튼을 비활성화합니다.
# disabled=True이면 버튼을 눌러도 실행할 수 없고,
# disabled=False이면 정상적으로 누를 수 있습니다.
# not has_raw는 has_raw가 False일 때 True가 되어 버튼을 막습니다.
if st.___("전처리 적용", disabled=not has_raw):
    # session_state에서 원본 DataFrame을 꺼내 저장된 전처리기에 전달합니다.
    # transform_members()는 새 데이터로 기준을 다시 배우지 않고
    # 2주차에서 저장한 기준만 적용해 처리 결과를 반환합니다.
    processed_members = transform_members(
        st.session_state["raw_members"],
        preprocessor,
    )

    # 처리 결과를 "processed_members" 키에 저장합니다.
    # 버튼을 눌러 화면 코드가 다시 실행되어도 다음 단계에서 다시 사용할 수 있습니다.
    st.session_state["processed_members"] = processed_members

if not has_raw:
    # 원본표가 아직 없으면 전처리 대신 다음에 할 행동을 안내합니다.
    st.info("먼저 데이터 가져오기를 실행해 주세요.")


# session_state에 처리 결과가 저장되었는지 확인합니다.
# has_processed는 처리 결과가 있으면 True, 없으면 False인 bool 변수입니다.
has_processed = "processed_members" in st.session_state
if has_processed:
    # 저장해 둔 처리 DataFrame을 현재 코드의 processed_members 이름으로 꺼냅니다.
    processed_members = st.session_state["processed_members"]

    # 처리 결과의 행 수와 열 수를 화면의 숫자 카드로 보여 줍니다.
    st.metric("처리 회원 수", len(processed_members))
    # shape는 (행 수, 열 수) tuple이므로 [1]로 열 수를 선택합니다.
    st.metric("처리 열 수", processed_members.shape[___])


# ============================= Q4 =============================
# Q4의 목표는 전처리 결과를 SQLite에 저장하고,
# 지금까지 DB에 누적된 행 수를 화면에서 확인하는 것입니다.
st.header("3. 저장 현황")

# 처리 결과가 없으면 DB에 저장할 자료가 없으므로 버튼을 비활성화합니다.
if st.___("DB에 저장", disabled=not has_processed):
    # 원본표와 처리표를 save_processed()에 넘깁니다.
    # 함수 안에서 collection_id와 식별 정보가 붙은 행이 만들어져 DB에 추가됩니다.
    save_processed(
        st.session_state["processed_members"],
        st.session_state["raw_members"],
        engine,
    )


# 첫 실행처럼 processed_members 테이블이 아직 없을 때도 화면이 멈추지 않게 준비합니다.
# inspect(engine)는 DB 구조를 살펴보는 SQLAlchemy 검사 객체를 만듭니다.
# get_table_names()는 현재 SQLite 파일에 존재하는 테이블 이름 list를 반환합니다.
tables = inspect(engine).get_table_names()
if "processed_members" in tables:
    # SQL의 COUNT(*)로 processed_members 테이블의 전체 행 수를 셉니다.
    # pd.read_sql_query()는 SQL 조회 결과를 DataFrame으로 반환합니다.
    # AS row_count는 계산 결과 열 이름을 row_count로 정합니다.
    # .loc[0, "row_count"]는 결과표의 첫 행과 row_count 열이 만나는 숫자를 꺼냅니다.
    row_count = pd.read_sql_query(
        ___,
        engine,
    ).loc[___, "row_count"]
else:
    # 테이블이 아직 없으면 저장된 행이 없으므로 화면에 0을 표시합니다.
    row_count = 0

# 현재 SQLite DB에 누적되어 있는 처리 행 수를 화면에 표시합니다.
st.metric("DB 누적 행 수", row_count)


# ============================= Q5 =============================
# Q5의 목표는 원본 회원표를 사용해 만든 그래프와 PCA 결과를
# Streamlit 화면에서 확인하는 것입니다.
st.header("4. 분석 보기")

if has_raw:
    # 화면이 다시 실행되어도 session_state의 현재 원본표를 분석 입력으로 사용합니다.
    raw_members = st.session_state["raw_members"]

    # make_activity_figure()는 week3_common.py에 미리 만든 그래프 함수입니다.
    # 원본표에서 활동 그래프를 만들고 Matplotlib Figure 객체를 반환합니다.
    figure = make_activity_figure(raw_members)

    # st.pyplot()은 이미 만들어진 Matplotlib Figure 객체를 브라우저에 표시합니다.
    # 그래프를 다시 계산하는 함수가 아니라 figure에 들어 있는 그림을 화면에 보여 줍니다.
    st.pyplot(figure)

    # make_pca_result()는 원본표를 PCA로 변환한 결과 DataFrame과 PCA 객체를 함께 반환합니다.
    # 왼쪽 변수 pca_result에는 PC1·PC2와 회원 식별 정보가 담긴 DataFrame이 들어가고,
    # 오른쪽 변수 pca에는 설명 비율 등을 확인할 PCA 객체가 들어갑니다.
    pca_result, pca = make_pca_result(raw_members)

    # PCA의 PC1과 PC2가 원래 숫자 열의 변동을 얼마나 설명하는지 계산합니다.
    # explained_variance_ratio_는 PCA 객체의 속성이고,
    # sum()으로 두 축의 설명 비율을 더한 뒤 100을 곱해 백분율로 바꿉니다.
    st.write(
        "PCA 두 축 설명력",
        round(pca.explained_variance_ratio_.___() * 100, ___),
        "%",
    )

    # PCA 결과 DataFrame의 앞부분을 브라우저 표로 표시합니다.
    # head()는 결과표 자체를 바꾸지 않고 미리 볼 행만 반환합니다.
    st.dataframe(pca_result.___(___))
else:
    # 원본표가 없으면 그래프와 PCA를 계산할 입력이 없습니다.
    # 사용자가 먼저 Q2의 데이터 가져오기를 실행하도록 안내합니다.
    st.info("데이터를 가져오면 그래프와 PCA 결과가 나타납니다.")
