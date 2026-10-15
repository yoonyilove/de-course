"""3주차 6교시 · 숫자 열 9개를 두 축으로 요약하기.

회원 100명의 숫자 열 9개를 PCA의 PC1·PC2로 바꿉니다.
그래프 PNG는 week3/outputs/figures/pca_members.png에 저장됩니다.
"""


from pathlib import Path
import sys
import pandas as pd

HERE = Path(__file__).resolve()
WEEK3_DIR = HERE.parents[1]
if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))


# 그림판과 축을 만들고 PNG로 저장하는데 필요한  Matplotlib.pyplot 을 plt 별칭으로 불러옵니다. 
# 3주차 5교시를 보고 써보세요. 
import matplotlib.pyplot as plt

# 박스플롯과 산점도를 그려주는 Seaborn을 sns 별칭으로 불러옵니다. 
# 3주차 5교시를 보고 써보세요. 
import seaborn as sns

# sklearn은 머신러닝 도구를 모아 둔 Python 라이브러리입니다.
# sklearn 뒤의 점(.)은 라이브러리 안의 하위 모듈로 들어간다는 뜻입니다.

# sklearn.impute는 결측치(imputation)를 처리하는 하위 모듈입니다.
# 그 안에 있는 SimpleImputer 클래스를 가져옵니다.
# from A import B는 A라는 모듈에서 B라는 도구를 가져오라는 문법입니다.
# 2주차 6교시를 참고해서 써보세요. 
from sklearn.impute import SimpleImputer


# sklearn.preprocessing은 데이터를 모델에 넣기 전에
# 전처리하는 도구들을 모아 둔 하위 모듈입니다.
# 그 안에서 숫자 크기를 맞추는 StandardScaler 클래스를 가져옵니다.
# 2주차 6교시를 참고해서 써보세요. 
from sklearn.preprocessing import StandardScaler


# sklearn.decomposition은 많은 열의 정보를
# 더 적은 수의 축으로 줄이는 도구들을 모아 둔 하위 모듈입니다.
# 그 안에서 주성분 분석(PCA)을 수행하는 PCA 클래스를 가져옵니다.
from sklearn.decomposition import PCA

# 공통 파일에서 숫자 열 이름 목록과 그래프 저장 폴더, 한글 글꼴 설정 함수를 가져옵니다.
from week3_common import (
    DATA_DIR, FIGURE_DIR, NUMERIC_FEATURES, configure_plot_fonts,
)

# 그래프 제목과 축에 한글이 표시되도록 이 교시에서만 글꼴을 설정합니다.
# 3주차 5교시를 보고 써보세요. 
configure_plot_fonts()

# 그래프 PNG를 넣을 폴더가 없다면 만듭니다. 파일 저장은 아직 하지 않습니다.
# mkdir(parents=True, exist_ok=True)는 폴더가 없으면 생성하고, 있으면 그냥 넘어갑니다.
# 3주차 5교시를 보고 써보세요. 
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# pd.read_csv()는 api_members_fallback.csv 파일을 읽어 
# 표 형태의 DataFrame으로 만들어, raw_members에 저장합니다. 
# 3주차 5교시를 보고 써보세요. 
raw_members = pd.read_csv(DATA_DIR / "api_members_fallback.csv")


# ------------------------------
# Q1. PCA에 넣을 숫자 열 9개만 원본 회원표에서 고릅니다.
#     - NUMERIC_FEATURES 목록으로 PCA에 넣을 숫자 열만 고르고, isna().sum()으로 빈값을 확인합니다.
# ------------------------------
# NUMERIC_FEATURES는 PCA에 사용할 열 이름이 순서대로 들어 있는 Python list입니다.
# DataFrame 뒤의 대괄호에 이 list를 넣으면 list에 적힌 순서의 9열짜리 새 DataFrame이 됩니다.
# copy()는 원본 raw_members를 직접 바꾸지 않고 별도의 표를 만들기 위해 사용합니다.
pca_input = raw_members[NUMERIC_FEATURES].copy()

# shape는 (행 수, 열 수) 형태의 tuple입니다. 여기서는 회원 수와 PCA 입력 열 수를 확인합니다.
print("PCA 입력 크기:", pca_input.shape)

# isna()는 pca_input의 각 칸이 빈값인지 True·False로 표시합니다.
# 결과는 원본과 같은 크기의 DataFrame입니다.
#
# sum()은 각 열에서 True의 개수를 더해 빈값 개수를 계산합니다.
# 그 결과 missing_by_column은 열 이름을 index로 갖는 Pandas Series입니다.
# Series의 각 값은 해당 열의 결측치 개수입니다.
#
# > 0은 결측치 개수가 1개 이상인지 검사합니다.
# 결과는 열 이름별 True·False가 들어 있는 조건 Series입니다.
# 이 조건으로 missing_by_column을 다시 고르면
# 빈값이 한 개라도 있는 열만 남습니다.
missing_by_column = pca_input.isna().sum()


# > 0 조건으로 빈값이 한 개라도 있는 열만 남깁니다. 
print("빈값이 있는 숫자 열:", missing_by_column[missing_by_column > 0])


# ------------------------------
# Q2. 빈 숫자값을 채운 뒤 열마다 숫자 크기를 맞춥니다.
#     - SimpleImputer로 빈값을 중앙값으로 채우고, 
#       StandardScaler로 열마다 숫자 크기를 맞춥니다. fit_transform()도 사용합니다.
# ------------------------------

# PCA를 실행하기 전에 숫자 표를 먼저 정리해야 합니다.
# 현재 pca_input에는 회원 100명의 숫자 열 9개가 들어 있습니다.
#
# 먼저 빈값을 채울 규칙을 정합니다.
# SimpleImputer는 결측치를 지정한 기준값으로 채우는 scikit-learn 도구입니다.
# strategy="median"은 각 열의 중앙값을 해당 열의 빈칸에 넣겠다는 뜻입니다.
#
# imputer는 SimpleImputer 객체를 저장하는 변수입니다.
# 아직 pca_input에 실제로 적용된 것은 아니며,
# 앞으로 사용할 결측치 처리 규칙을 담고 있습니다.
imputer = SimpleImputer(strategy="median")


# fit_transform()은 두 작업을 한 번에 실행합니다.
# 1. fit: pca_input의 각 열을 살펴보고 열별 중앙값을 계산해 기억합니다.
# 2. transform: 기억한 중앙값으로 빈값을 채웁니다.
#
# filled_values는 결측치가 채워진 결과를 저장하는 변수입니다.
# 입력 pca_input은 Pandas DataFrame이지만,
# SimpleImputer의 결과는 보통 NumPy 배열입니다.
# 따라서 filled_values의 모양은 (100, 9)입니다.
filled_values = imputer.fit_transform(pca_input)


# 결측치를 채운 뒤에는 숫자 열들의 크기를 비슷한 기준으로 맞춥니다.
# 열마다 단위나 값의 범위가 다르면 큰 숫자를 가진 열이
# PCA 결과에 지나치게 큰 영향을 줄 수 있기 때문입니다.
#
# StandardScaler는 각 열의 평균과 표준편차를 이용해
# 값을 평균 0, 표준편차 1에 가까운 기준으로 변환하는 도구입니다.
#
# scaler는 StandardScaler 객체를 저장하는 변수입니다.
# 이후 학습한 평균과 표준편차를 기억하고 재사용할 수 있습니다.
scaler = StandardScaler()


# filled_values에 StandardScaler를 적용합니다.
# fit: filled_values의 각 열에서 평균과 표준편차를 계산해 기억합니다.
# transform: 그 기준으로 각 숫자를 변환합니다.
#
# scaled_values는 크기가 맞춰진 결과를 저장하는 변수입니다.
# 이 결과도 NumPy 배열이며, 행과 열의 수는 그대로 (100, 9)입니다.
# 이제 이 값을 PCA에 입력할 수 있습니다.
scaled_values = scaler.fit_transform(filled_values)


# shape는 배열의 모양을 나타내는 속성입니다.
# (100, 9)가 출력되면 회원 100명과 숫자 열 9개가
# 그대로 유지되었다는 뜻입니다.
print("크기를 맞춘 배열:", scaled_values.shape)


# mean(axis=0)은 각 열의 평균을 계산합니다.
# axis=0은 행들을 위아래로 모아 열별로 계산하라는 뜻입니다.
# 따라서 결과에는 숫자 열 9개의 평균이 각각 하나씩 들어갑니다.
#
# StandardScaler를 올바르게 적용했다면 열별 평균은 0에 가까워야 합니다.
# 단, 컴퓨터의 부동소수점 계산 때문에 정확히 0이 아니라
# 1e-16처럼 아주 작은 숫자가 나올 수 있습니다.
#
# round(6)은 계산 결과를 소수점 아래 6자리까지 반올림해
# 화면에서 읽기 쉽게 표시합니다.
# 이 값은 데이터를 다시 반올림하는 것이 아니라 출력 모양만 정리합니다.
print("열별 평균:", scaled_values.mean(axis=0).round(6))


# ------------------------------
# Q3. 9개의 숫자 열로 표현된 회원 정보를 PCA로 학습하고, 회원마다 PC1·PC2 두 개의 좌표를 만드는 것입니다.
# ------------------------------
# 앞 단계에서 결측치를 채우고 숫자 크기를 맞춘 scaled_values를
# PCA에 입력합니다.
#
# PCA는 여러 숫자 열에 함께 나타나는 변화를 분석해
# 원래 열보다 적은 수의 새로운 축으로 요약하는 도구입니다.
# 새 축은 PC1, PC2처럼 이름이 붙으며,
# 각 회원은 각 축에 해당하는 숫자 좌표를 갖게 됩니다.
#
# n_components=2는 새 축을 2개만 만들겠다는 설정입니다.
# 따라서 회원 한 명의 9개 숫자 정보가
# PC1 값 하나와 PC2 값 하나로 요약됩니다.
#
# random_state=42는 무작위 계산 과정이 사용될 때
# 결과를 매번 같은 방식으로 재현하기 위한 기준 숫자입니다.
# 42라는 숫자 자체에 특별한 의미가 있는 것은 아니며,
# 한 번 정한 값을 계속 사용하면 됩니다.
#
# pca는 PCA 객체를 저장하는 변수입니다.
# 나중에 설명 비율을 확인하거나 새 데이터에 같은 축을 적용할 때 사용합니다.
pca = PCA(n_components=2, random_state=42)


# fit_transform()은 두 작업을 한 번에 실행합니다.
# 1. fit: scaled_values의 숫자 구조를 분석해 PC1·PC2 축을 계산합니다.
# 2. transform: 각 회원의 값을 계산된 두 축의 좌표로 바꿉니다.
#
# coordinates는 변환 결과를 저장하는 변수입니다.
# 입력은 NumPy 배열 scaled_values이고,
# 결과도 NumPy 배열입니다.
# 회원 순서는 유지되며 각 행은 기존 회원 한 명에 대응합니다.
coordinates = pca.fit_transform(scaled_values)


# shape는 NumPy 배열의 모양을 나타내는 속성입니다.
# 원래 scaled_values가 (100, 9)이었다면
# PCA 결과는 (100, 2)가 되어야 합니다.
# 즉, 회원 100명의 정보가 PC1·PC2 두 열로 바뀌었는지 확인합니다.
print("회원 좌표 크기:", coordinates.shape)


# 앞의 세 회원이 두 PCA 축에서 어떤 좌표를 갖는지 확인합니다.
# NumPy 배열에서 [:3]은 행의 처음 세 개를 선택하는 슬라이싱입니다.
# 콜론 뒤의 열 범위를 생략했으므로 PC1과 PC2 두 열을 모두 보여 줍니다.
print("앞 세 회원의 PC1·PC2 좌표:\n", coordinates[:3])


# ------------------------------
# Q4. 두 축이 원래 9개 숫자 열의 차이를 얼마나 설명하는지 확인합니다.
#    - explained_variance_ratio_로 PC1과 PC2가 원래 데이터의 변동을 얼마나 설명하는지 확인합니다.
# ------------------------------
# explained_variance_ratio_는 PCA 객체가 계산해 둔 속성입니다.
# PC1과 PC2가 원래 데이터의 변동을 각각 어느 정도 설명하는지
# 비율로 저장한 NumPy 배열입니다.
explained = pca.explained_variance_ratio_

# 두 축의 설명 비율을 더해
# PC1과 PC2를 함께 사용했을 때 원래 데이터의 변동을
# 얼마나 설명하는지 계산합니다.
total_explained = explained.sum()

# round(4)는 화면에 소수점 아래 네 자리까지 표시하라는 뜻입니다.
print("축별 설명 비율:", explained.round(4))
print("두 축의 설명 비율 합:", round(total_explained, 4))

# 현재 수업용 데이터에서는 다음과 비슷한 결과가 나옵니다.
# 축별 설명 비율: [0.6284 0.1234]
# 두 축의 설명 비율 합: 0.7519
#
# PC1은 원래 데이터 변동의 약 62.84%를 설명합니다.
# PC2는 약 12.34%를 추가로 설명합니다.
# PC1과 PC2를 합치면 약 75.19%를 설명합니다.
#
# 이 값은 예측 정확도가 아니라,
# 9개의 숫자 열을 두 개의 PCA 축으로 줄였을 때
# 원래 데이터의 차이와 변동을 얼마나 보존했는지를 나타냅니다.


# ------------------------------
# Q5. PCA 결과를 사람이 해석할 수 있는 표와 그림으로 바꿔봅니다. 
#     - PCA 좌표를 DataFrame으로 만들고 회원 ID와 등급을 붙인 뒤, 
#       sns.scatterplot()으로 회원 분포를 그래프로 확인합니다.
# ------------------------------
# coordinates는 PCA가 반환한 NumPy 배열입니다.
# 배열에는 100명의 PC1·PC2 숫자가 들어 있지만,
# NumPy 배열 자체에는 열 이름이 없습니다.
#
# pd.DataFrame()은 NumPy 배열을 Pandas DataFrame으로 바꾸는 함수입니다.
# columns=["PC1", "PC2"]는 두 열에 직접 이름을 붙이는 설정입니다.
# 첫 번째 열의 이름은 PC1, 두 번째 열의 이름은 PC2가 됩니다.
#
# pca_result는 회원 100명과 PCA 좌표 2개를 가진 DataFrame입니다.
pca_result = pd.DataFrame(
    coordinates,
    columns=["PC1", "PC2"],
)


# PCA 계산에는 회원 ID를 넣지 않았으므로 좌표표에도 ID가 없습니다.
# 그래프나 결과를 해석할 때 어느 회원의 좌표인지 알 수 있도록 ID를 다시 붙입니다.
#
# insert()는 DataFrame에 새 열을 원하는 위치에 넣는 메소드입니다.
# 첫 번째 인수 0: 새 열을 넣을 위치입니다. 0은 맨 앞을 뜻합니다.
# 두 번째 인수 "member_id": 새 열의 이름입니다.
# 세 번째 인수 raw_members["member_id"]: 새 열에 넣을 값입니다.
#
# 결과 열 순서는 member_id, PC1, PC2가 됩니다.
# raw_members와 coordinates의 행 순서가 같다는 전제에서
# 각 회원의 ID와 PCA 좌표가 올바르게 연결됩니다.
pca_result.insert(
    0,
    "member_id",
    raw_members["member_id"],
)


# membership_tier는 PCA 계산에 사용하지 않은 원본 정보입니다.
# PCA 결과를 등급별로 비교하기 위해 결과표에 별도 열로 추가합니다.
# 대괄호로 새 열 이름을 지정하고 Series를 대입하면 DataFrame 열이 만들어집니다.
pca_result["membership_tier"] = raw_members["membership_tier"]


# PCA 결과를 그림으로 그릴 Figure와 Axes를 만듭니다.
# plt.subplots()는 두 객체를 tuple로 반환합니다.
# figure_pca는 전체 그림 영역(Figure)이고,
# axes_pca는 실제 그래프가 그려질 좌표 영역(Axes)입니다.
# figsize=(8, 5)는 그림의 가로·세로 크기를 인치 단위로 지정합니다.
figure_pca, axes_pca = plt.subplots(figsize=(8, 5))


# Seaborn의 scatterplot()으로 PCA 결과를 산점도로 그립니다.
# pca_result의 각 행, 즉 회원 한 명이 그래프의 점 하나가 됩니다.
sns.scatterplot(
    # 점을 만들 때 사용할 DataFrame입니다.
    data=pca_result,

    # DataFrame의 PC1 열을 가로축으로 사용합니다.
    x="PC1",

    # DataFrame의 PC2 열을 세로축으로 사용합니다.
    y="PC2",

    # membership_tier 값에 따라 점의 색상을 다르게 표시합니다.
    # 같은 등급의 회원들이 어느 위치에 모이는지 비교할 수 있습니다.
    hue="membership_tier",

    # 방금 만든 axes_pca 영역에 그래프를 그립니다.
    ax=axes_pca,
)


# Axes 객체의 set_title() 메소드로 그래프 제목을 지정합니다.
axes_pca.set_title("회원의 PCA 두 축")

# 그래프 PNG를 저장할 파일의 위치를 만듭니다.
# FIGURE_DIR은 그래프 폴더를 나타내는 Path 객체입니다.
# / 연산자는 폴더 경로와 파일 이름을 이어 새 Path를 만듭니다.
pca_path = FIGURE_DIR / "pca_members.png"

# Figure 전체를 PNG 파일로 저장합니다.
# savefig()는 Figure 객체에 그려진 그래프를 파일로 내보내는 메서드입니다.
# bbox_inches="tight"는 그래프 주변의 불필요한 여백을 줄이고
# 제목이나 축 이름이 잘리지 않도록 저장하라는 설정입니다.
figure_pca.savefig(pca_path, bbox_inches="tight")

# 저장이 끝난 Figure를 닫아 메모리에서 정리합니다.
# 앞 교시를 보고 비슷하게 채워보세요. 
plt.close(figure_pca)

# PCA 결과표의 행·열 크기와 저장된 그림의 위치를 확인합니다.
print("결과표 크기:", pca_result.shape)
print("PCA 그림 저장:", pca_path)

# 이 교시의 모든 코드가 오류 없이 끝났다는 표시를 출력합니다.
print("[PASS] 3주차 6교시 완료")
