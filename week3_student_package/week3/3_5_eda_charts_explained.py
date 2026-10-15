"""3주차 5교시 · 저장된 회원 데이터를 살펴보고 그래프로 확인하기.

4교시의 연습용 DB가 있으면 첫 번째 수집분 100명만 읽습니다.
DB 테이블이 아직 없으면 제공 CSV로 첫 번째 수집분을 준비합니다.
그래프 PNG는 week3/outputs/figures 폴더에 저장됩니다.
"""


from pathlib import Path
import sys
import pandas as pd

HERE = Path(__file__).resolve()

WEEK3_DIR = HERE.parents[1]

if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))


# Matplotlib.pyplot 을 plt 별칭으로 불러옵니다. 
# 그림판과 축을 만들고 PNG로 저장하는데 필요합니다. 
import matplotlib.pyplot as plt

# Seaborn을 sns 별칭으로 불러옵니다. 
# 박스플롯과 산점도를 그리는데 필요합니다. 
import seaborn as sns

# SQLAlchemy에서 데이터베이스 연결과 구조 확인에 필요한 두 기능 
# create_engine, inspect를 가져옵니다. 
# create_engine은 Python 코드가 SQLite 파일에 연결할 수 있도록
# 데이터베이스 연결 설정 객체인 engine을 만드는 함수입니다.
# inspect는 engine에 연결된 데이터베이스를 살펴보는 함수입니다.
# 두 이름을 함께 가져오므로 from 뒤의 import 목록에
# create_engine과 inspect를 쉼표로 나란히 적습니다.
from sqlalchemy import create_engine, inspect

# 공통 데이터·DB·그림 폴더와 한글 글꼴 설정 함수를 가져옵니다.
from week3_common import DATA_DIR, DATABASE_DIR, FIGURE_DIR, configure_plot_fonts

# configure_plot_fonts()는 week3_common.py에 미리 정의된 함수입니다.
# 괄호를 붙여 함수를 실제로 실행합니다.
# 그래프를 만들기 전에 한글 글꼴 설정 함수를 실행합니다.
# 함수가 AppleGothic, Malgun Gothic, NanumGothic 등을 확인하고
# 사용할 수 있는 글꼴을 Matplotlib 설정에 등록합니다.
# 또한 그래프의 음수 기호가 깨지지 않도록 관련 설정도 적용합니다.
configure_plot_fonts()

# SQLite DB와 그래프 PNG를 넣을 폴더가 없다면 만듭니다. 파일 저장은 아직 하지 않습니다.
# 각 폴더의 이름은 DATABASE_DIR, FIGURE_DIR 로 합니다. 
# mkdir(parents=True, exist_ok=True)는 폴더가 없으면 생성하고, 있으면 그냥 넘어갑니다.
# 앞 2개 교시를 참고해서 적어보세요. 
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# 1교시에서 제공한 100명짜리 대체 CSV입니다.
raw_fallback = pd.read_csv(DATA_DIR / "api_members_fallback.csv")

# 4교시와 같은 연습용 DB 파일을 가리킵니다.
# 4교시 결과를 5교시에서 이어서 분석하려고 일부러 같은 파일을 사용하는 것입니다.
# 5교시는 그중 member_snapshots를 읽어 EDA를 합니다.
db_path = DATABASE_DIR / "lesson4_practice.db"
engine = create_engine(f"sqlite:///{db_path}")

# DB의 member_snapshots 테이블이 아직 없을 때만 수업용 100행을 준비합니다.
# 테이블이 이미 있으면 4교시에서 저장한 내용을 그대로 사용합니다.
if "member_snapshots" not in inspect(engine).get_table_names():
    source = raw_fallback.copy()
    source.insert(0, "collection_id", "lesson4_first")
    source.to_sql("member_snapshots", engine, if_exists="replace", index=False)

# ------------------------------
# Q1. 같은 수집분의 회원 100명만 분석 대상으로 고릅니다.
#     - SQL의 WHERE로 분석할 수집분을 고르고, 결측치를 확인합니다.
# ------------------------------

# 4교시의 두 번째 실습에서 추가한 10행은 이번 분석에 섞지 않습니다.
# 즉, collection_id가 "lesson4_first"인 첫 번째 수집분만 골라 분석합니다.
# 즉, 4교시 Q5에서 추가한 "lesson4_second" 10행은 제외한다는 말입니다. 
# 
# 이번에 read_sql_query로 반환받는 dataframe은 analysis_data란 변수를 만들어 저장합니다. 
# SELECT *는 member_snapshots 테이블의 모든 열을 가져오라는 뜻입니다.
# WHERE 조건은 collection_id가 "lesson4_first"인 행만 고르라는 뜻입니다.
#
# engine은 연결할 SQLite 데이터베이스를 알고 있는 SQLAlchemy 연결 객체입니다.

analysis_data = pd.read_sql_query(
    "SELECT * FROM member_snapshots WHERE collection_id = 'lesson4_first'",
    engine,
)
# print를 사용하여, 반환받은 Dataframe의 크기를 표시해보세요. 
# shape는 DataFrame의 모양을 (행 수, 열 수) tuple로 보여 줍니다.
# 예: (100, 17)은 회원 100명과 열 17개라는 뜻입니다.
print("분석표 크기:", analysis_data.shape)


# 분석과 그래프를 만들기 전에 결측치가 있는지 먼저 확인합니다.
# 빈값이 많으면 평균·집계·그래프 결과가 실제와 다르게 보일 수 있습니다.
# 어떤 열에 빈값이 몇 개인지 알아야 삭제·대체·별도 처리 여부를 결정할 수 있습니다.
#
# isna()는 analysis_data의 모든 셀이 비어 있는지 검사합니다.
# 비어 있으면 True, 값이 있으면 False인 같은 크기의 DataFrame을 반환합니다.
#
# sum()은 각 열을 아래 방향으로 더합니다.
# True는 1, False는 0처럼 계산되므로
# 결과는 각 열에 빈값이 몇 개인지 나타내는 Series가 됩니다.
missing_by_column = analysis_data.isna().sum()

# missing_by_column > 0은 각 열의 결측치 개수가 1개 이상인지 검사합니다.
# 결과는 열 이름마다 True 또는 False가 들어 있는 조건 mask입니다.
#
# missing_by_column[조건]은 조건이 True인 열만 골라 냅니다.
# 따라서 결측치가 한 개라도 있는 열 이름과 결측치 개수만 출력합니다.
print(
    "빈값이 있는 열:",
    missing_by_column[missing_by_column > 0],
)

# 현재 교육용 데이터에 결측치가 없다면 빈 Series가 출력됩니다.
# 이것은 오류가 아니라 “빈값이 있는 열이 없다”는 뜻입니다.


# ------------------------------
# Q2. 그림을 그리기 전에 활동일 수의 범위와 가운데 값을 읽습니다.
#     : describe()로 숫자 열의 개수·평균·중앙값·범위를 요약합니다.
# ------------------------------

# 활동일 수의 분포를 살펴보기 전에 숫자 요약부터 확인합니다.
# active_days 열 하나를 대괄호[]로 고르면 회원별 활동일 수만 담은 Pandas Series가 됩니다.
#
# describe()는 Series의 숫자값을 요약하는 Pandas 메소드입니다.
# 소괄호()를 붙여 실행하면 개수(count), 평균(mean), 표준편차(std),
# 최솟값(min), 25%·50%·75% 지점, 최댓값(max)을 계산합니다.
#
# 반환된 요약 결과는 숫자 하나가 아니라 
# 여러 항목 이름을 index로 가진 Series이며 active_summary에 저장합니다. 
active_summary = analysis_data["active_days"].describe()

# 요약 Series의 각 항목과 계산된 값을 화면에 표시합니다.
print("활동일 요약:\n", active_summary)

# describe() 결과에서 "50%"라는 이름의 항목을 선택합니다.
# 50% 지점은 전체 회원을 활동일 수 순서로 세웠을 때 가운데에 있는 값,
# 즉 중앙값(median)을 뜻합니다.
# 대괄호 안의 "50%"는 Series의 index 이름입니다.
print("중앙값:", active_summary["50%"])

# ------------------------------
# Q3. 히스토그램으로 회원의 활동일 수가 어디에 몰리는지 봅니다.
#     - matplotlib으로 활동일 수의 분포를 히스토그램으로 그려 저장합니다.
# ------------------------------

# 그래프 전체와 그래프를 실제로 그릴 공간을 함께 만듭니다.
# plt.subplots()는 Figure 객체와 Axes 객체를 묶어서 돌려줍니다.
# figure는 그림 전체, axes는 실제 그래프가 그려지는 영역입니다.
# figsize=(8, 4)는 가로 8인치, 세로 4인치입니다. figsize는 Figure Size의 줄임말입니다.
# 오른쪽에서 반환된 두 값을 왼쪽 변수에 순서대로 나눠 저장합니다.
# 첫 번째 값인 Figure는 그래프 전체를,
# 두 번째 값인 Axes는 제목·축·막대를 그릴 공간을 뜻합니다.
figure_hist, axes_hist = plt.subplots(figsize=(8, 4))

# axes_hist는 DataFrame이나 Series 같은 자료구조가 아니라, Matplotlib의 Axes 객체입니다.
# analysis_data["active_days"]는 회원별로 30일 동안 로그인한 날짜 수를 담은 Series입니다.
# hist()는 이 숫자들을 구간별로 나누어 히스토그램으로 그립니다.
# bins=10은 전체 값의 범위를 10개 구간으로 나눈다는 뜻입니다.
# bins=10은 활동일 수 범위를 열 구간으로 나눠 회원 수를 세라는 뜻입니다. 
# color="#2563EB"는 막대 색상을 파란색으로 지정합니다.
axes_hist.hist(analysis_data["active_days"], bins=10, color="#2563EB")

# 그래프의 제목을 지정합니다.
axes_hist.set_title("회원 100명의 30일 활동일 분포")

# 가로축이 무엇을 뜻하는지 표시합니다.
axes_hist.set_xlabel("로그인한 날짜 수")

# 세로축이 각 구간에 속한 회원 수임을 표시합니다.
axes_hist.set_ylabel("회원 수")

# 그림 파일의 주소를 만든 뒤 PNG로 저장합니다.


# 그래프를 저장할 파일의 위치를 만듭니다.
# FIGURE_DIR은 그래프를 저장할 폴더를 가리키는 Path 객체입니다.
# Path 객체에서 / 연산자는 폴더와 파일 이름을 이어 새 경로를 만듭니다.
# 아직 파일을 저장한 것은 아니고, 저장할 주소만 hist_path에 넣습니다.
hist_path = FIGURE_DIR / "active_days_histogram.png"

# figure_hist는 그래프 전체 그림을 관리하는 Figure 객체입니다. 
# 그럼 이제 figure_hist에 그려진 히스토그램을 PNG 이미지 파일로 저장해보겠습니다. 
# savefig()는 Figure 객체에 포함된 그래프를 파일로 내보내는 메서드입니다.
# hist_path를 넣었으므로 지정한 폴더와 파일 이름으로 저장됩니다.
# bbox_inches="tight"는 그래프 주변의 불필요한 여백을 줄여
# 제목이나 축 이름이 잘리지 않도록 저장하라는 설정입니다. bounding box의 줄임말
figure_hist.savefig(hist_path, bbox_inches="tight")

# 저장이 끝난 그래프를 메모리에서 닫습니다.
# plt.close()는 화면에 표시하는 기능이 아니라
# 사용이 끝난 Figure 객체를 정리하는 Matplotlib 함수입니다.
# 그래프를 여러 개 만들 때 메모리가 계속 쌓이는 것을 막기 위해 사용합니다.
plt.close(figure_hist)

# 저장된 경로를 터미널에 출력하여 어느 위치에 어떤 이름으로 저장되었는지 확인합니다.
print("히스토그램 저장:", hist_path)

# ------------------------------
# Q4. 회원권 등급별 앱 실행 수를 박스플롯으로 비교합니다.
#     - groupby()로 회원권 등급별 수치를 요약하고, seaborn 박스플롯으로 분포를 비교합니다.
# ------------------------------

# 회원권 등급별로 앱 실행 수를 비교하기 위해 등급을 기준으로 회원을 묶습니다.
# groupby("membership_tier")는 같은 등급의 행들을 하나의 그룹으로 묶는
# Pandas GroupBy 객체, tier_summary를 만듭니다. 
#
# 그 뒤의 agg()는 각 그룹에서 여러 계산을 한 번에 실행하는 Pandas 메소드입니다.
# agg 안에서는 새로 만들 결과 열 이름과
# 계산에 사용할 원본 열·계산 방법을 함께 적습니다.
#
# members=("member_id", "count")
# → 각 회원권 등급에 속한 member_id의 개수를 세어
#   결과 열 이름을 members로 만듭니다.
#
# median_app_opens=("total_app_opens", "median")
# → 각 회원권 등급의 total_app_opens 중앙값을 계산해
#   결과 열 이름을 median_app_opens로 만듭니다.
#
# 계산 결과는 행이 membership_tier별 등급이고,
# 열이 members와 median_app_opens인 새로운 DataFrame, tier_summary입니다.
# 2주차 4교시 문제2번을 보고 참고해서 써보세요. 
tier_summary = analysis_data.groupby("membership_tier").agg(
    members=("member_id", "count"),
    median_app_opens=("total_app_opens", "median"),
)

# 완성된 등급별 요약 DataFrame을 print로 화면에 표시합니다.
print("등급별 요약:\n", tier_summary)

# boxplot은 원본 DataFrame에서 등급 열을 가로축, 실행 수를 세로축에 씁니다.
# 위의 groupby 결과는 숫자 요약을 읽기 위한 표이지 그림의 필수 입력은 아닙니다.

# 박스플롯을 그릴 전체 Figure와 실제 그래프 공간 Axes를 만듭니다.
# plt.subplots()는 두 객체를 함께 반환합니다.
# figure_box는 그래프 전체를,
# axes_box는 제목·축·박스플롯을 그릴 공간을 가리킵니다.
#
# figsize=(8, 4)는 그래프 크기를 가로 8인치, 세로 4인치로 지정합니다.
figure_box, axes_box = plt.subplots(figsize=(8, 4))

# 회원 등급별 앱 실행 횟수를 박스플롯으로 그립니다.
# 회원권 등급마다 앱 실행 횟수의 분포가 어떻게 다른가? 를 보기위한 것입니다. 

# Seaborn을 sns라는 짧은 이름으로 위에서 가져왔었습니다. 
# sns.boxplot()은 숫자값의 분포를 박스 모양으로 그리는 Seaborn 함수입니다.
# 괄호 안에 DataFrame과 사용할 열, 그래프를 그릴 영역을 지정합니다.
sns.boxplot(
    # 그래프에 사용할 전체 DataFrame을 data에 전달합니다.
    # analysis_data는 회원별 활동 정보가 들어 있는 Pandas DataFrame입니다.
    data=analysis_data,

    # x에는 가로축에 배치할 열 이름을 문자열로 적습니다.
    # membership_tier의 값이 회원 등급별 그룹을 만듭니다.
    # 같은 등급의 회원들은 하나의 박스 안에서 함께 비교됩니다.
    x="membership_tier",

    # y에는 세로축에 배치할 숫자 열 이름을 문자열로 적습니다.
    # 각 회원의 total_app_opens 값을 등급별로 나누어
    # 앱 실행 횟수의 분포를 비교합니다.
    y="total_app_opens",

    # ax에는 그래프를 그릴 Matplotlib Axes 객체를 전달합니다.
    # axes_box는 앞에서 plt.subplots()로 만든 그래프 영역입니다.
    # 이 값을 지정하면 Seaborn 그래프가 axes_box 영역에 그려집니다.
    ax=axes_box,
)
# axes_box 그래프 영역의 제목을 설정합니다.
# set_title()은 Axes 객체의 메소드이며,
# 괄호 안의 문자열이 그래프 위쪽 제목으로 표시됩니다.
axes_box.set_title("회원권별 앱 실행 수")

# 박스플롯을 저장할 PNG 파일의 위치를 만듭니다.
# FIGURE_DIR은 그래프 폴더를 나타내는 Path 객체입니다.
# / 연산자는 폴더 경로와 파일 이름을 이어 새 Path를 만듭니다.
# 이 줄에서는 아직 그림을 저장하지 않고 저장 위치만 정합니다.
box_path = FIGURE_DIR / "app_opens_by_tier_boxplot.png"

# Figure 전체를 PNG 파일로 저장합니다.
# savefig()는 Figure 객체에 그려진 그래프를 파일로 내보내는 메서드입니다.
# bbox_inches="tight"는 그래프 주변의 불필요한 여백을 줄이고
# 제목이나 축 이름이 잘리지 않도록 저장하라는 설정입니다. bounding box의 줄임말
figure_box.savefig(box_path, bbox_inches="tight")

# 사용이 끝난 Figure를 닫아 메모리에서 정리합니다.
# 그래프를 여러 개 만들 때 이전 Figure가 계속 남지 않도록 합니다.
plt.close(figure_box)

# 그래프가 저장된 경로를 터미널에 출력합니다.
print("박스플롯 저장:", box_path)


# ------------------------------
# Q5. 프로필 조회와 추천 조회가 함께 늘어나는지 점으로 확인합니다.
#     - corr()로 두 숫자 열의 관계를 계산하고, 산점도로 함께 나타냅니다. 
# ------------------------------

# 상관관계를 비교할 숫자 열 두 개만 선택합니다.
# 대괄호를 두 겹으로 쓰고 열 이름 list를 넣으면
# 결과가 Series가 아니라 두 열을 가진 작은 DataFrame이 됩니다.
#
# 첫 번째 열은 회원별 프로필 조회 수이고,
# 두 번째 열은 회원별 추천 조회 수입니다.
comparison_data = analysis_data[
    [
        "total_profile_views",
        "total_recommendations_viewed",
    ]
]

# corr()는 DataFrame의 숫자 열들 사이의 상관계수를 계산하는 Pandas 메소드입니다.
# 결과는 숫자 하나가 아니라 각 열을 행과 열에 함께 배치한
# 상관관계 표(DataFrame)로 반환됩니다.
#
# 결과 표의 구조는 다음과 같습니다.
#
#                                  total_profile_views
# total_profile_views                         1.0
# total_recommendations_viewed                상관계수
#
# 같은 열끼리 비교한 대각선 값은 항상 1.0입니다.
# 서로 다른 두 열이 만나는 칸의 값이
# 프로필 조회 수와 추천 조회 수가 함께 늘어나는 정도를 나타냅니다.
#
# 상관계수는 보통 -1부터 1 사이의 값입니다.
# 1에 가까우면 함께 증가하고, 0에 가까우면 뚜렷한 직선 관계가 약하며,
# -1에 가까우면 한쪽이 늘 때 다른 쪽이 줄어드는 경향을 뜻합니다.
correlation_table = comparison_data.corr()


# correlation_table에서 상관계수를 꺼내 correlation이라는 변수에 저장하겠습니다. 
# iloc[0, 1]은 행 위치 0번, 열 위치 1번의 값을 고르는 문법입니다.
# 즉, 첫 번째 열과 두 번째 열 사이의 상관계수를 꺼냅니다.
correlation = correlation_table.iloc[0, 1]

# 상관계수를 소수 셋째 자리까지 반올림하여 출력합니다.
# round()의 두 번째 값 3은 소수점 아래 세 자리까지 표시하라는 뜻입니다.
print("두 조회 수의 상관계수:", round(correlation, 3))


# 산점도는 회원 한 명을 점 하나로 나타내는 그래프입니다.
# x축에는 프로필 조회 수를, y축에는 추천 조회 수를 배치합니다.
# Figure는 그래프 전체를, Axes는 실제로 점을 그릴 공간을 뜻합니다.
figure_scatter, axes_scatter = plt.subplots(figsize=(8, 4))

# Seaborn의 scatterplot() 함수를 사용해 산점도를 그립니다.
# 산점도는 DataFrame의 각 행을 점 하나로 표시하여
# 두 숫자 열이 함께 어떻게 움직이는지 보여 주는 그래프입니다.
sns.scatterplot(
    # 점을 만들 때 사용할 전체 DataFrame을 전달합니다.
    # analysis_data의 한 행은 회원 한 명의 기록입니다.
    data=analysis_data,

    # x에는 가로축으로 사용할 열 이름을 문자열로 적습니다.
    # 회원별 total_profile_views 값이 가로축의 위치가 됩니다.
    x="total_profile_views",

    # y에는 세로축으로 사용할 열 이름을 문자열로 적습니다.
    # 회원별 total_recommendations_viewed 값이 세로축의 위치가 됩니다.
    y="total_recommendations_viewed",

    # ax에는 그래프를 그릴 Matplotlib Axes 객체를 전달합니다.
    # axes_scatter는 앞에서 plt.subplots()로 만든 그래프 영역입니다.
    # 이 값을 지정하면 산점도가 해당 영역에 그려집니다.
    ax=axes_scatter,
)

# axes_scatter 그래프 영역의 제목을 설정합니다.
# set_title()은 Axes 객체의 메소드이며,
# 괄호 안의 문자열이 그래프 위쪽에 제목으로 표시됩니다.
axes_scatter.set_title("프로필 조회와 추천 조회")

# 산점도를 저장할 PNG 파일의 위치를 만듭니다.
# FIGURE_DIR은 그래프 저장 폴더를 나타내는 Path 객체입니다.
# / 연산자는 폴더 경로와 파일 이름을 이어 새 Path를 만듭니다.
scatter_path = FIGURE_DIR / "profile_vs_recommendation_scatter.png"

# 그래프 전체를 PNG 이미지로 저장합니다.
# bbox_inches="tight"는 주변의 불필요한 여백을 줄여 제목과 축 이름이 잘리지 않도록 합니다. bounding box의 줄임말
figure_scatter.savefig(scatter_path, bbox_inches="tight")

# 저장이 끝난 Figure를 닫아 메모리에서 정리합니다. 
plt.close(figure_scatter)

# 산점도가 실제로 저장된 위치를 터미널에 출력합니다.
print("산점도 저장:", scatter_path)

# 이 교시의 모든 코드가 오류 없이 끝났다는 표시를 출력합니다.
print("[PASS] 3주차 5교시 완료")