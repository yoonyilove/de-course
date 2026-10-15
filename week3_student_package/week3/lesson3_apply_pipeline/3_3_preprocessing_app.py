"""3주차 3교시 · 저장된 전처리기로 새 회원 데이터 처리

이 파일을 Streamlit으로 실행하면 새 회원 100명에게 2주차에 저장한
전처리 규칙을 적용하고, 결과를 화면에서 확인해 CSV로 저장할 수 있습니다.
"""

from pathlib import Path
import sys

HERE = Path(__file__).resolve()

WEEK3_DIR = HERE.parents[1]

if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))

import pandas as pd
import streamlit as st


# 저장된 전처리기 객체를 파일에서 불러오기 위해 joblib 라이브러리를 가져옵니다.
# 2주차 6교시 참고해보세요. 
import joblib

# 저장 파일의 이름에 현재 날짜와 시각을 넣을 때 사용합니다. datetime 모듈을 가져옵니다.
# 3주차 1교시 참고해보세요. 
from datetime import datetime

# 공통 파일에서 데이터·전처리기·결과 폴더와 입력 열 목록을 가져옵니다. 즉, 
# week3_common.py 파일에서 DATA_DIR, ARTIFACT_DIR, PROCESSED_DIR, INPUT_FEATURES 변수를 가져옵니다.
from week3_common import DATA_DIR, ARTIFACT_DIR, PROCESSED_DIR, INPUT_FEATURES


# 수업에서 제공한 대체 CSV의 위치입니다.
# 프로젝트 기준: matchmaking_data/03_week3/api_members_fallback.csv
# DATA_DIR은 폴더 위치를 담은 Path 객체이고, CSV의 주소를 만들 때 사용합니다.
raw_path = DATA_DIR / "api_members_fallback.csv"

# 2주차에 학습하고 저장한 전처리기 파일을 3주차용으로 준비해두었습니다. 
# ARTIFACT_DIR 폴더에 matchmaking_preprocessor.joblib 파일을 가져옵니다.
artifact_path = ARTIFACT_DIR / "matchmaking_preprocessor.joblib"

# 전처리 한 결과 CSV를 넣을 폴더가 없다면 만듭니다.
# 이 폴더는 학생이 3주차 3교시에서 전처리 결과를 저장하면서 처음 사용합니다.
# 폴더의 경로객체 이름은 PROCESSED_DIR로 정합니다. 
# mkdir()은 Path 객체가 가리키는 폴더를 만드는 메소드입니다.
# parents=True는 필요한 상위 폴더도 함께 만들고, exist_ok=True는 폴더가 이미 있어도 괜찮다는 뜻입니다. 오류를 내지 않습니다.
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# 브라우저의 탭 제목과 화면 너비를 정합니다.
# set_page_config는 브라우저의 탭 제목과 화면 너비를 정합니다.
# page_title은 브라우저 탭의 제목을 설정합니다. "저장된 전처리기 적용"
# layout="wide"는 브라우저 화면을 너비 100%로 설정합니다.
# 3주차 2교시 파일을 참고해서 써보세요. 
st.set_page_config(page_title="저장된 전처리기 적용", layout="wide")

# 브라우저 화면에 이번 교시의 제목과 목표를 보여 줍니다.
# 제목은 "저장된 전처리기 적용" 입니다. 
# title은 브라우저 화면의 제목을 설정합니다. title은 한 번만 사용할 수 있습니다.
# write는 브라우저 화면에 텍스트를 출력합니다. 줄바꿈을 하고 싶으면 \n을 사용합니다.
# writ 안에 "2주차에 저장한 기준을 새 회원 데이터에 적용해 봅니다."을 적어보세요. 
# 3주차 2교시 파일을 참고해서 써보세요. 
st.title("저장된 전처리기 적용")
st.write("2주차에 저장한 기준을 새 회원 데이터에 적용해 봅니다.")

# CSV 파일을 읽어 회원 100명 × 16열의 DataFrame을 만듭니다.
# raw_members는 회원 100명 × 16열의 DataFrame입니다.
# raw_path는 파일의 경로를 나타내는 Path 객체입니다.
# read_csv는 CSV 파일을 읽어 DataFrame으로 변환합니다.
raw_members = pd.read_csv(raw_path)


# ------------------------------
# Q1. 저장된 전처리기를 다시 불러옵니다.
# ------------------------------

# artifact_path는 저장해 둔 전처리기 파일의 위치를 나타내는 Path 객체입니다.
# joblib.load()는 그 위치의 .joblib 파일을 읽어
# 파일 안에 저장된 Python 객체를 메모리로 다시 불러옵니다.
#
# 이 파일 안에는 회원 데이터 표가 들어 있는 것이 아닙니다.
# 2주차에서 학습한 전처리기 객체가 들어 있습니다.
# 예를 들어 숫자 열의 중앙값·평균·표준편차와 문자 열에서 보았던 범주 목록 등의 기준을 기억하고 있습니다.
#
# 불러온 객체를 preprocessor라는 변수에 저장합니다.
preprocessor = joblib.load(artifact_path)

# type()은 괄호 안에 있는 객체의 자료형, 즉 어떤 클래스에서 만들어졌는지 확인하는
# Python 내장 함수입니다.
#
# preprocessor가 회원 DataFrame인지, 단순 문자열인지,
# 아니면 ColumnTransformer 객체인지 확인합니다.
# 저장한 전처리기를 제대로 불러왔는지 점검하는 용도입니다.
print(type(preprocessor))


# ------------------------------
# Q2. 전처리에 필요한 열이 있는지 확인합니다.
# ------------------------------

# INPUT_FEATURES는 week3_common.py 파일에서 미리 준비된 열 이름 목록입니다.
# INPUT_FEATURES에는 전처리기가 요구하는 열 이름 13개가 순서대로 있습니다.
# 이번 교시 코드 상단에서 import로 필요한 부분을 읽어들일 때 포함되어 있었습니다. 
#
# raw_members.columns는 위에서 읽어들인 원본표의 열 이름 목록입니다. 
# raw_members.columns는 raw_members DataFrame이 자동으로 갖게 되는 속성정보입니다.
# raw_members.columns는 리스트는 아니고, Pandas의 Index 객체입니다. 하지만 리스트처럼 사용이 가능합니다. 
# 일반 리스트가 꼭 필요하면 .tolist()를 붙입니다. 예: raw_members.columns.tolist()
# 목록을 하나씩 읽어 원본표에 없는 이름만 missing_columns에 모읍니다.
# INPUT_FEATURES에서 열 이름을 하나씩 꺼내 name이라고 부릅니다. 그 이름이 raw_members.columns에 없으면 missing_columns에 넣습니다.
missing_columns = [
    name for name in INPUT_FEATURES
    if name not in raw_members.columns
]

# 필요한 열이 하나라도 빠졌다면, 이름을 보여 주고 여기서 실행을 멈춥니다.
# st.error는 Streamlit 화면에 빨간색 오류 안내 상자를 보여줍니다.
# 단, st.error()만 쓰면 화면에 오류를 보여준 뒤에도 아래 코드가 계속 실행됩니다.
#
# missing_columns는 원본표에 없는 열 이름을 모아 둔 Python list입니다.
# 예: ["age", "gender"]처럼 문자열 여러 개가 들어갈 수 있습니다.
#
# if 뒤의 조건이 비어 있지 않으면 아래 들여쓴 코드를 실행합니다.
# 빈 list []는 False로, 하나라도 들어 있는 list는 True로 판단됩니다.

if missing_columns:
    # f로 시작하는 문자열은 f-string입니다.
    # 중괄호 {missing_columns} 안의 변수값을 문장에 넣어 줍니다.
    # 여기서 {}는 dict를 만드는 기호가 아니라, 값을 끼워 넣을 자리입니다.
    # 예: ["age"]가 들어 있으면
    # "전처리에 필요한 열이 없습니다: ['age']"처럼 표시됩니다.
    st.error(f"전처리에 필요한 열이 없습니다: {missing_columns}")

    # st.stop은 현재 Streamlit 실행을 그 자리에서 멈춥니다. 
    # 따라서 필요한 열이 없는데도 전처리를 계속 진행하지 않도록 막습니다.
    st.stop()


# ------------------------------
# Q3. 버튼을 누르면 새 회원표에 전처리 규칙을 적용합니다.
# ------------------------------

# st.button()은 버튼을 만들고, 이번 실행에서 버튼이 눌렸는지를 True 또는 False로 돌려줍니다.
# 버튼을 누르지 않았으면 False이므로 if 아래 들여쓴 코드가 실행되지 않습니다.
# button은 클릭한 실행에서 True를 돌려주고, 아래 코드를 실행합니다. 
# 버튼에 표시될 내용은 "저장된 기준으로 전처리"로 표시합니다. 
if st.button("저장된 기준으로 전처리"):

    # 16열짜리 raw_members에서 INPUT_FEATURES 리스트에 적힌 13열만 골라서, 
    # 리스트에 적힌 순서대로 새 DataFrame, new_X를 만듭니다.
    new_X = raw_members[INPUT_FEATURES]

    # transform은 new_X에 저장된 기준을 적용합니다. 
    processed_members = preprocessor.transform(new_X)

    # Streamlit은 버튼을 누를 때마다 Python 파일을 처음부터 다시 실행합니다.
    # session_state는 같은 브라우저 세션 동안 이전 실행의 값을 보관하는 저장 공간입니다.
    # 디스크에 파일로 저장하는 것이 아니라, 현재 사용자의 화면이 이어지는 동안만 보관합니다.  
    # 이전 단계의 DataFrame을 이름별로 보관해 두며, 딕셔녀리 형태로 저장합니다. 

    # 아래 코드에서 우리는 원본 표와 전처리 결과를 각각 다시 보여줄 수 있도록 따로 저장합니다.  
    # session_state 안의 "raw_members"라는 이름표(key)에, 현재 변수 raw_members의 DataFrame을 넣습니다.
    # session_state 안의 "processed_members"라는 이름표(key)에, 전처리 결과인 DataFrame을 넣습니다.
    st.session_state["raw_members"] = raw_members
    st.session_state["processed_members"] = processed_members


# ------------------------------
# Q4. 원본표와 처리표를 나란히 확인합니다.
# ------------------------------

# 처리 결과가 상태에 있을 때만 아래 화면과 CSV 저장 버튼을 표시합니다.
if "processed_members" in st.session_state:

    # 앞에서 session_state에 보관한 두 DataFrame을 별도의 이름으로 꺼냅니다.
    # raw_members, Session State의 키, stored_raw_members는 
    # 하나의 DataFrame을 가리키는 서로 다른 이름 또는 저장 위치 입니다. 
    # CSV에서 다시 읽은 raw_members 변수의 내용을 덮어쓰지 않도록 stored_ 이름을 사용합니다.

    # raw_members  ─────────┐
    #                       ├── 같은 DataFrame 객체
    # st.session_state      │
    # ["raw_members"] ──────┘
    #                       │
    # stored_raw_members ───┘

    stored_raw_members = st.session_state["raw_members"]
    stored_processed_members = st.session_state["processed_members"]



    # 원본은 16열, 처리 결과는 36열입니다. 행 수는 100명입니다. 
    # stored_raw_members 와 stored_processed_members의 크기를,
    # Write, shape을 확용해서 확인해보세요. 
    st.write("원본표 크기:", stored_raw_members.shape)
    st.write("처리표 크기:", stored_processed_members.shape)

    # st.metric은 Streamlit 화면에 중요한 숫자를 카드 형태로 크게 보여 줍니다.
    # 첫 번째 값은 카드 제목이고, 두 번째 값은 카드에 표시할 숫자입니다. st.metric("제목", 값) 형식으로 사용합니다.
    # 첫 번째 카드는 처리된 DataFrame의 행 수를 보여 주도록 코드를 작성해보세요. 
    # 3주차 2교시에서 배웠으니 참고해서 써보세요. 
    st.metric("처리 회원 수", len(stored_processed_members))

    # 두 번째 카드는 처리된 DataFrame의 열 수를 보여 주도록 코드를 작성해보세요. 
    # shape는 결과가 튜플 자료형입니다. 열 개수를 가져오려면 []안에 무엇을 넣어야 할까요. 튜플의 두 번째 숫자를 골라야 합니다. 
    st.metric("처리 열 수", stored_processed_members.shape[1])

    # 두 표를 같은 화면에서 비교할 수 있도록 브라우저를 두 칸으로 나눕니다.
    # st.columns(2)는 브라우저 화면을 같은 너비의 두 칸으로 나눕니다.
    # 반환된 두 화면 영역을 왼쪽은 left, 오른쪽은 right라는 변수에 나누어 담습니다.
    left, right = st.columns(2)

    # left는 화면을 나눈 뒤 만든 왼쪽 영역입니다.
    # with는 Python의 문법이고, left는 Streamlit이 만든 화면 영역 객체입니다.
    # with는 특정 작업 범위를 정하는 문법입니다. 콜론 뒤에 들여쓴 코드가 그 범위 안에서 실행됩니다.
    # with left: 아래에 들여쓴 Streamlit 명령은 왼쪽 영역 안에 표시됩니다.

    with left:

        # st.subheader는 화면 안에 작은 제목을 표시합니다.
        # 여기서는 왼쪽에 보여 주는 표가 전처리 전 표라는 것을 알려 줍니다.
        st.subheader("처리 전")

        # st.caption은 제목보다 작은 보조 설명을 표시합니다. 
        # st.caption은 글자가 작고 연한색으로 표시됩니다. 
        # 이 표가 사람이 읽는 원본 회원 정보이고, 열이 16개라는 것을 설명합니다.
        st.caption("사람이 읽는 원본 회원 정보 · 16열")

        # stored_raw_members는 Session State에서 꺼낸 원본 회원 DataFrame입니다.
        # head(3)은 Pandas DataFrame 메소드이며, 표의 위에서부터 3행만 골라
        # 화면에 보여 줄 작은 DataFrame을 새로 반환합니다.
        # 원본 DataFrame의 행을 삭제하거나 수정하지는 않습니다.
        preview_raw = stored_raw_members.head(3)

        # preview_raw를 화면에 표시해 보겠습니다. 
        # st.dataframe()은 Streamlit 함수입니다.
        # DataFrame을 브라우저 화면에 표 형태로 표시합니다.
        # st.dataframe()의 st는 import streamlit as st에서 만든 별칭입니다.
        #
        # use_container_width=True는 표를 고정된 좁은 폭으로 두지 않고
        # 화면의 사용 가능한 너비에 맞춰 넓게 표시하라는 설정입니다.
        st.dataframe(preview_raw, use_container_width=True)

    with right:
        st.subheader("처리 후")
        st.caption("계산과 모델 입력에 사용할 숫자표 · 36열")
        st.dataframe(stored_processed_members.head(3), use_container_width=True)

    # st.info()는 Streamlit이 제공하는 화면 표시 함수입니다.
    # 일반 글자보다 눈에 띄는 파란색 안내 상자를 브라우저에 보여 줍니다.
    # 오류를 뜻하는 기능은 아니며, 다음 단계에 대한 설명이나 참고사항을 전달할 때 사용합니다.
    #
    # 여기서는 오른쪽에 표시된 전처리 결과가 이후 모델·그래프·DB 작업의 입력으로 사용된다는 점을 알려 줍니다.
    st.info("오른쪽 처리 결과가 다음 단계에서 사용할 입력표입니다.")

    # ------------------------------
    # Q6. 처리 결과를 CSV 파일로 저장합니다.
    # ------------------------------

    if st.button("처리 결과 CSV 저장"):

        # 저장 시각을 파일 이름에 넣어 결과 파일을 구분합니다.
        # Python 표준 라이브러리 datetime의 now() 기능으로 현재 날짜와 시각을 가져오겠습니다. 
        # datetime은 Python 표준 라이브러리 datetime에서 가져온 날짜·시간 클래스입니다.
        # datetime.now()는 이 클래스를 사용해 현재 날짜와 시각을 datetime 객체로 만듭니다.
        # 그 뒤의 strftime()은 방금 만들어진 datetime 객체에 적용하는 메서드입니다.
        # string format time의 줄임말이며, 날짜·시간을 지정한 문자열 형식으로 바꿉니다.
        # strftime()은 날짜·시간을 20261012_153000 같은 파일 이름용 문자열로 바꿉니다.
        # %Y  → 네 자리 연도, %m  → 두 자리 월, %d  → 두 자리 일
        # %H  → 시, %M  → 분, %S  → 초, 중간의 _는 파일 이름에서 날짜와 시각을 구분하기 위한 일반 문자입니다.
        # 최종 결과는 예를 들어 "20261012_153000" 같은 문자열이 됩니다.
        # processed_20261013_143508.csv와 같은 형식으로 파일 이름을 만들고 싶은 것입니다. 
        # 이 문자열을 processed_at이라는 변수에 저장합니다.
        # 3주차 1교시 코드를 보고 적어보세요. 
        processed_at = datetime.now().strftime("%Y%m%d_%H%M%S")


        # 처리 결과를 저장할 파일의 경로 객체를 만듭니다.
        # PROCESSED_DIR은 week3_common.py에서 가져온 결과 폴더의 Path 객체입니다.
        # / 연산자는 결과 폴더 경로와 파일 이름을 이어 새 Path 객체를 만듭니다.
        # f-string의 {processed_at} 자리에는 현재 처리 시각 문자열이 들어갑니다.
        # 따라서 processed_20261015_143000.csv와 같은 파일 이름이 만들어집니다.
        # 완성된 경로는 processed_path 변수에 저장됩니다.
        # 이 줄은 파일을 저장하는 것이 아니라 저장 위치를 정하는 단계입니다.
        processed_path = PROCESSED_DIR / f"processed_{processed_at}.csv"

        # st.success를 이용해 저장이 끝났다는 안내문 "저장했습니다"를 브라우저 화면에 초록색 메시지로 보여 줍니다.
        # processed_path.name은 전체 경로가 아니라 파일 이름만 가져옵니다.
        # 3주차 2교시 코드를 보고 적어보세요.  
        stored_processed_members.to_csv(processed_path, index=False)
        st.success(f"저장했습니다: {processed_path.name}")
else:
    # 위에서 공부한 info를 사용하여, "전처리 버튼을 먼저 눌러주세요."라는 안내문을 표시되게 해보세요. 
    st.info("전처리 버튼을 먼저 눌러 주세요.")
