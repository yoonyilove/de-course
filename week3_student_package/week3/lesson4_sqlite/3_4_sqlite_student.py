"""3주차 4교시 · 회원표를 SQLite 데이터베이스에 저장하고 SQL로 확인하기

이 파일은 3교시에서 준비한 원본 회원표와 전처리 결과를
연습용 SQLite 파일에 서로 다른 테이블로 저장하고 다시 조회합니다.

Q2의 if_exists="replace"는 같은 이름의 기존 연습 테이블을 현재 표로 바꿉니다.
실무 데이터베이스에 그대로 사용하면 기존 데이터가 사라질 수 있으므로,
이 수업에서는 lesson4_practice.db라는 연습용 파일에만 사용합니다.
"""

from pathlib import Path
import sys

HERE = Path(__file__).resolve()
WEEK3_DIR = HERE.parents[1]

if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))

import pandas as pd

# create_engine은 Python 코드와 데이터베이스 사이의 연결 설정 객체를 만드는 SQLAlchemy 함수입니다.
# sqlalchemy 라이브러리에서 이 함수 하나만 가져옵니다.
from ____ import ____

# week3_common.py에 미리 준비된 폴더 경로와 지원 함수를 가져옵니다. 
# from 뒤에 .py를 쓰지 않아도, Python이 자동으로 같은 폴더나 검색 경로에서 찾습니다. 
# 가져올 것이 많아서 소괄호 () 로 담아옵니다. 객체와 함수가 같이 담겨도 됩니다. 
# DATA_DIR: 수업용 CSV가 들어 있는 폴더를 가리키는 Path 객체
# DATABASE_DIR: SQLite 파일을 저장할 폴더를 가리키는 Path 객체
# load_preprocessor(): 저장된 전처리기 객체를 불러오는 함수
# transform_members(): 원본 회원표에 저장된 전처리 규칙을 적용하는 함수
# add_collection_columns(): 처리표에 수집 ID와 회원 확인용 열을 붙이는 함수
# 3주차 3교시 코드를 보고 한번 적어보세요. 
from week3_common import (
    DATA_DIR, DATABASE_DIR, load_preprocessor,
    transform_members, add_collection_columns,
)


# DB를 저장할 때가 되었으니 필요한 폴더를 만들겠습니다. 이미 만들어져 있으면 그대로 사용하자고 설정해주겠습니다. 
# mkdir()은 Path 객체가 가리키는 폴더를 만드는 메소드입니다.
# parents=True는 필요한 상위 폴더도 함께 만들고, exist_ok=True는 폴더가 이미 있어도 괜찮다는 뜻입니다. 오류를 내지 않습니다.
DATABASE_DIR.____(parents=___, exist_ok=___)

raw_members = pd.read_csv(DATA_DIR / "api_members_fallback.csv")

# 위에서 week3_common.py로부터 가져온 load_preprocessor() 함수를 실행합니다.
# load_preprocessor()는 week3_common.py에 미리 정의된 Python 함수입니다.
# 괄호가 비어 있는 이유는 파일 위치가 함수 안에 이미 정해져 있어 전달할 값이 없기 때문입니다.
# 함수가 저장된 전처리기 파일을 읽어 반환하면, 그 결과를 preprocessor 변수에 저장합니다.
# 반환된 preprocessor는 회원표가 아니라 중앙값·평균·표준편차·범주 목록을 기억하는 전처리기 객체입니다.
preprocessor = ____

# 위에서 불러온 transform_members()를 실행하여 결과를 저장합니다. 
# transform_members()에는 raw_members DataFrame과 위에서 만든 전처리기 객체 preprocessor를 전달합니다
# 함수 안에서는 필요한 13열을 골라 preprocessor.transform()을 적용하게 되어있습니다. 
# processed_members에 전처리된 회원 100명 × 전처리된 숫자 36열의 DataFrame을 저장합니다. 
processed_members = ____(____, ____)

# collection_id라는 문자열 별수를 만들어서, 같은 시점에 함께 수집한 행들을 구분해보겠습니다. 
# 3주차 4교시에서는 데이터가 시간에 따라 여러 번 들어오는 상황을 흉내 내고 있습니다.
# api_members_fallback.csv에서 읽은 회원 100명을 “첫 번째로 받은 데이터”라고 가정합니다
# "lesson4_first"는 첫 번째 수집분이라는 뜻으로 만든 문자열이고, collection_id에 넣어줍니다. 
collection_id = ____

# DATABASE_DIR과 파일 이름을 / 연산자로 이어 SQLite 파일의 저장 위치를 만듭니다.
# 저장할 SQlite 파일의 이름은 "lesson4_practice.db"로 하기로 합니다. 
# db_path는 아직 데이터베이스 내용이 아니라 lesson4_practice.db의 위치를 나타내는 Path 객체입니다.
db_path = DATABASE_DIR / ____


# ------------------------------
# Q1. Python과 SQLite를 연결할 engine 만들기 
#     - SQLite 파일을 사용할 연결 설정 객체를 만듭니다.
# ------------------------------

# create_engine()은 SQLAlchemy 함수이며, 소괄호 안에 데이터베이스 연결 주소를 받습니다.
# f-string 안의 {db_path} 자리에는 위에서 만든 SQLite 파일 경로가 들어갑니다.
# sqlite:///는 "이 컴퓨터의 SQLite 파일에 연결한다"는 SQLAlchemy의 주소 형식입니다.
# engine은 데이터표가 아니라, 앞으로 어느 DB에 SQL을 보내고 저장할지 기억하는 연결 설정 객체입니다.
engine = ____(f"____:///{____}")

# type()은 객체의 자료형을 확인하는 Python 내장함수입니다.
# 실행 결과에서 engine이 SQLAlchemy의 Engine 객체인지 print로 확인해봅니다. 
print("연결 객체 자료형:", ____(engine))

# db_path에 DB 파일이 있는지 없는지 exist()로 확인하고, print로 그 내용을 표시해봅니다. 
# exists()는 Path 객체가 가리키는 파일이 현재 디스크에 실제로 있는지 True 또는 False로 알려 주는 메소드입니다.
# 연결 설정만 만든 직후에는 DB 파일이 아직 없을 수도 있으며, 아래에서 표를 저장할 때 실제 파일이 만들어집니다.
print("현재 DB 파일 존재 여부:", ____.____)


# ------------------------------
# Q2. SQL 문장을 직접 쓰지 않고 Pandas 표를 DB 테이블로 저장하기
#     - 원본표와 전처리표를 서로 다른 DB 테이블에 저장합니다.
#       원본표는 받은 당시의 모습을 보존하고, 전처리표는 계산·분석·모델 입력에 사용하기 위해 서로 다른 DB 테이블에 나누어 저장합니다.
# ------------------------------

# copy()는 DataFrame의 복사본을 만드는 Pandas 메소드입니다.
# 복사본에 열을 추가해도 원래 raw_members가 바뀌지 않도록 raw_for_db라는 이름으로 복사본을 만들어 봅니다. 
raw_for_db = ____.copy()

# insert()는 DataFrame의 원하는 위치에 새 열을 넣는 Pandas 메소드입니다.
# 괄호 안에는 보통 세 가지 값을 순서대로 넣습니다.
# 첫 번째 값 0: 새 열을 넣을 위치입니다. 0은 가장 앞이라는 뜻입니다.
# 두 번째 값 "collection_id": 새로 만들 열의 이름입니다.
# 세 번째 값 collection_id: 새 열에 넣을 값입니다.
# 하나의 문자열을 넣으면 모든 행에 같은 값이 반복해서 들어갑니다.
# 따라서 100개 행 모두에 "lesson4_first"가 들어간 collection_id 열이 생깁니다.
raw_for_db.____(___, ____, ____)

# add_collection_columns()는 week3_common.py에 미리 정의된 지원 함수입니다.
# 전처리 결과표에는 회원을 알아볼 ID와 수집 정보가 없을 수 있으므로(숫자·원핫인코딩 열이 중심이므로)
# 원본표의 member_id, residence_region, membership_tier와
# 현재 수집분을 나타내는 collection_id를 처리표 앞에 붙입니다.
# 원래 processed_members를 바꾸지 않도록 복사본을 만든 뒤 작업하고,
# 완성된 DB를 저장용 DataFrame인 processed_for_db에 담습니다.
processed_for_db = ____(
    processed_members, raw_members, collection_id
)

# [중요] to_sql()은 DataFrame을 데이터베이스 테이블로 저장하는 Pandas 메소드입니다.
# raw_for_db는 DB에 저장할 준비가 끝난 Python DataFrame입니다.
# 문자열 "member_snapshots"는 우리가 저장할때 쓰려고 정한 DB 테이블 이름입니다.
# member는 회원 데이터, snapshots는 특정 시점에 저장해 둔 데이터의 모습을 뜻합니다.
# Python 변수 raw_for_db의 이름과 DB 테이블 이름이 자동으로 같아지는 것은 아니라는 점을 명심하세요. 
# engine은 연결할 SQLite 파일의 위치와 연결 방법을 알고 있는 객체입니다. 우리가 위에서 만들었습니다. 
# if_exists="replace"는 같은 이름의 연습 테이블이 있으면 지우고 현재 DataFrame으로 다시 만듭니다.
# index=False는 DataFrame의 0~99 행 번호를 별도 DB 열로 저장하지 않는 설정입니다.
raw_for_db.____(
    "member_snapshots", engine, if_exists=___, index=___
)

# 전처리된 DataFrame도 같은 방식으로 저장하되, DB 테이블 이름은 "processed_members"로 정합니다.
# 따라서 하나의 lesson4_practice.db 안에 원본용 테이블과 전처리 결과용 테이블이 따로 생깁니다.
# 물리적으로는 SQLite 파일 하나 안에 표 두 개가 들어가는 것입니다.
#   lesson4_practice.db   -> 파일 하나
#   ├── member_snapshots  -> 원본 회원표
#   └── processed_members -> 전처리 결과표 
processed_for_db.____(
    ____, ____, if_exists=___, index=___
)


# ------------------------------
# Q3. SQL의 SELECT, COUNT, FROM, AS로 DB에 저장된 행 수 조회하기
#     - SQL로 원본 테이블의 행 수를 세어 확인합니다.
#     - Q2에서 DataFrame을 DB 테이블로 저장했기 때문에, DB 안에 실제로 저장된 행 수를 SQL로 확인해봅니다. 
# ------------------------------

# pd.read_sql_query()는 SQL 문장을 DB에 보내고,
# 조회 결과를 Pandas DataFrame으로 받아오는 함수입니다.
#
# SQL 조회 결과는 Pandas 표로 변환됩니다.
# COUNT(*)의 결과가 숫자 하나여도 DataFrame에서는 1행 × 1열 표가 됩니다.
#
# 첫 번째 인수는 실행할 SQL 문자열입니다.
# 두 번째 인수 engine은 SQL을 보낼 데이터베이스 연결 객체입니다.
#
# SELECT는 데이터를 조회하라는 SQL 명령입니다.
# COUNT(*)는 테이블의 전체 행 수를 세라는 뜻입니다.
# 여기서 *는 모든 행을 대상으로 삼으라는 표시입니다.
#
# AS row_count는 계산 결과가 들어갈 열 이름을 row_count로 정합니다.
# SQL은 Pandas처럼 행 이름을 만들지 않습니다.
# SQL 결과를 DataFrame으로 바꾸는 과정에서 Pandas가 결과 행에
# 자동으로 0이라는 index를 붙입니다.
#
# FROM member_snapshots는 member_snapshots 테이블에서 조회하라는 뜻입니다.
count_result = pd.read_sql_query(
    "SELECT COUNT(___) AS ____ FROM _____",
    engine,
)

print("행 수 결과표:", count_result)

# count_result는 SQL 조회 결과를 담은 1행 × 1열 DataFrame입니다.
# 열 이름은 "row_count", 행의 index는 Pandas가 자동으로 붙인 0입니다.
#
# .loc은 DataFrame에서 행 이름과 열 이름을 사용해 값을 고르는 접근자입니다.
# 메소드가 아니므로 loc 뒤에 ()를 쓰지 않고 []를 사용합니다.
#
# loc[행 이름, 열 이름] 형식으로 작성합니다.
# 0은 index가 0인 첫 번째 행을 뜻하고,
# "row_count"는 값을 가져올 열 이름을 뜻합니다.
#
# 따라서 loc[0, "row_count"]는
# 0번 행과 row_count 열이 만나는 칸의 숫자 하나를 꺼냅니다.
# count_result의 0번 행과 row_count 열이 만나는 행 수를 바로 출력합니다.
# print()는 꺼낸 행 수 숫자를 설명 문장과 함께 화면에 표시합니다.
print("저장된 원본 행 수:", ____.loc[___, ___])




# ------------------------------
# Q4. SQL의 WHERE 조건으로 서울 회원만 골라 DataFrame으로 받기
#     - SQL 조건으로 서울 회원만 골라 다시 DataFrame으로 받습니다.
# ------------------------------

# SELECT *는 모든 열을 가져오라는 뜻이고, FROM 뒤에는 조회할 테이블 이름을 씁니다.
# * 자체가 항상 열 또는 행만 의미하는 것은 아니고, 어떤 SQL 기능과 함께 쓰였는지에 따라 뜻이 달라지는 “전부” 표시입니다.
# WHERE는 가져올 행의 조건을 정하며, residence_region이 '서울'인 행만 남깁니다.
# SQL 문자열 안의 '서울'은 열 이름이 아니라 비교할 문자 값이므로 작은따옴표로 감쌉니다.
# 조회 결과는 원본 테이블의 일부 행으로 구성된 새 DataFrame이며 seoul_members에 담깁니다.
seoul_members = pd.read_sql_query(
    "SELECT __ FROM _____ WHERE r______ = '서울'",
    _____,
)

# shape는 DataFrame의 (행 수, 열 수)를 담은 tuple입니다.
# 따라서 이 출력으로 서울 회원이 몇 명이고 결과표에 열이 몇 개인지 확인합니다.
print("서울 회원표 크기:", seoul_members.___)

# seoul_members["residence_region"]은 지역 열 하나를 Series로 선택합니다.
# unique()는 Series에서 중복을 제거한 고유값을 보여 주는 Pandas 메소드입니다.
# WHERE 조건이 제대로 적용되었다면 결과에는 '서울'만 있어야 합니다.
print("지역 값:", seoul_members[___].____)


# ------------------------------
# Q5. Pandas로 추가 저장하고 SQL로 전체 행 수 확인하기
#     - 기존 테이블을 지우지 않고 두 번째 수집분을 아래에 추가합니다.
# ------------------------------

# head(10)은 원본 DataFrame의 첫 10행을 고르는 Pandas 메소드입니다.
# copy()로 별도 DataFrame을 만들어 원본 raw_members에는 영향을 주지 않습니다.
# 실제 신규 데이터 대신 저장 방식을 연습하기 위해 기존 회원 10명을 두 번째 수집분처럼 사용합니다.
second_batch = raw_members.____._____

# 두 번째 수집분임을 구분하도록 맨 앞에 collection_id 열을 추가합니다.
# "lesson4_second" 역시 우리가 정한 교육용 문자열이며, 10개 행에 같은 값이 들어갑니다.
second_batch.insert(0, "collection_id", "lesson4_second")

# if_exists="append"는 기존 member_snapshots 테이블을 지우지 않고 새 10행을 아래에 추가합니다.
# replace와 달리 기존 100행이 남으므로 저장 후 전체 행 수는 110이 됩니다.
# 이 실습은 추가 저장 방법을 보여 주며, 회원 ID 중복을 제거하는 단계는 포함하지 않습니다.
second_batch.to_sql(
    ______, _____, if_exists=___, index=___
)

# 같은 COUNT SQL을 다시 실행하여 member_snapshots에 
# 기존 100행과 추가된 10행이 모두 저장되었는지 확인합니다.
# new_count라는 이름의 변수에 반환된 Dataframe을 저장하시면 됩니다.  
# 문제3번을 보고 만들어보세요. 
new_count = ___.___(
    _______________________________________
)

# loc[0, "row_count"]으로 new_count 1행 × 1열 결과표 안의 숫자 하나를 꺼냅니다.
# 문제3번을 보고 만들버오세요. 
# 정상 결과는 110입니다.
print("추가 후 원본 행 수:", ___.___[___, ___])

# 모든 코드가 오류 없이 끝까지 실행되었음을 터미널에 표시합니다.
print("[PASS] 3주차 4교시 완료")
