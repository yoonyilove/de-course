# 함수의 자료형 주석을 나중에 해석하도록 미루는 Python 기능입니다.
# 이 파일에서는 Path, datetime, sqlite3.Connection처럼 다른 모듈의 자료형을
# 함수 설명에 적어도, 모듈을 읽는 시점에 불필요한 해석 문제가 생기지 않도록 합니다.
from __future__ import annotations

# 현재 날짜·시각을 만들 때 사용할 datetime 클래스를 가져옵니다.
# timestamp_text()가 파일 이름에 넣을 시각 문자열을 만드는 데 사용합니다.
from datetime import datetime

# 운영체제별 파일·폴더 주소를 문자열 대신 Path 객체로 다루는 도구입니다.
# 아래의 DATA_DIR, OUTPUT_DIR 같은 경로 변수와 / 연산에 사용합니다.
from pathlib import Path

# Python에 기본으로 포함된 SQLite 연결 모듈입니다.
# open_sqlite()의 반환 자료형을 설명하고 실제 DB 연결을 여는 데 사용합니다.
import sqlite3

# 숫자로 계산할 입력 열의 이름을 수업에서 직접 정한 Python list입니다.
# 이 이름들은 회원 원본표에서 전처리·PCA에 사용할 숫자 열을 선택할 때 재사용합니다.
# NUMERIC_FEATURES처럼 대문자로 쓴 것은 “여러 곳에서 바꾸지 않고 공유할 기준값”이라는
# 의미를 드러내기 위한 프로젝트 관례이며, Python이 강제로 상수로 만드는 문법은 아닙니다.
NUMERIC_FEATURES = [
    "age", "active_days", "total_app_opens", "total_stay_time_min",
    "total_profile_views", "total_recommendations_viewed",
    "total_messages_sent", "avg_reply_delay_sec", "days_since_last_activity",
]

# 숫자 계산보다 범주별 구분이 필요한 문자 열의 이름을 모아 둔 Python list입니다.
# 전처리기에서 원-핫 인코딩할 열을 같은 순서로 선택할 때 사용합니다.
CATEGORICAL_FEATURES = [
    "gender", "residence_region", "membership_tier", "signup_channel",
]

# 위 두 list를 이어 붙인 전체 입력 열 목록입니다.
# NUMERIC_FEATURES를 먼저, CATEGORICAL_FEATURES를 뒤에 두어
# 전처리기에 전달할 열의 순서까지 한 곳에서 고정합니다.
# INPUT_FEATURES는 우리가 만든 변수 이름이며, transform_members()가 반복해서 사용합니다.
INPUT_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES


def find_course_materials_dir() -> Path:
    """프로젝트 원본과 학생용 압축파일의 공통 자료 폴더를 찾아 반환합니다."""

    # 현재 작업 폴더가 아니라 이 파일의 위치를 기준으로 찾습니다.
    # 이렇게 하면 터미널을 어느 폴더에서 열었는지와 관계없이 작동합니다.
    here = Path(__file__).resolve().parent

    # week3_common.py가 들어 있는 폴더와 그 부모 폴더들을 아래에서 위로 확인합니다.
    candidates = [here, *here.parents]

    # 두 배포 구조를 모두 지원합니다.
    # 1) 프로젝트: course_materials/week3 + course_materials/matchmaking_data
    # 2) 학생용: week3_student_package/week3 + week3_student_package/matchmaking_data
    for base in candidates:
        for course_dir in (base, base / "course_materials"):
            has_week3 = (course_dir / "week3").is_dir()
            has_data = (course_dir / "matchmaking_data" / "03_week3").is_dir()
            if has_week3 and has_data:
                return course_dir

    # 어느 구조에서도 필요한 폴더를 찾지 못하면 경로 문제를 명확히 알립니다.
    raise FileNotFoundError(
        "week3와 matchmaking_data/03_week3가 함께 있는 자료 폴더를 찾지 못했습니다."
    )


# 위 함수가 찾아 준 공통 자료 폴더의 위치를 Path 객체로 저장합니다.
# COURSE_DIR은 이 파일에서 우리가 만든 경로 변수이며, 아래 모든 경로의 기준점입니다.
COURSE_DIR = find_course_materials_dir()

# 3주차 수업 파일들이 모여 있는 폴더를 가리키는 Path 객체입니다.
WEEK3_DIR = COURSE_DIR / "week3"

# 3주차에서 사용하는 원본·대체 CSV가 들어 있는 데이터 폴더입니다.
DATA_DIR = COURSE_DIR / "matchmaking_data" / "03_week3"

# 이미 학습해 둔 전처리기(joblib 등)를 읽을 폴더입니다.
# artifact는 이후 단계에서 다시 사용할 수 있도록 저장해 둔 결과물이라는 뜻입니다.
ARTIFACT_DIR = WEEK3_DIR / "artifacts"

# 수업 중 새로 만들어지는 결과물의 큰 기준 폴더입니다.
OUTPUT_DIR = WEEK3_DIR / "outputs"

# API에서 받은 가공 전 원본 CSV를 저장할 하위 폴더입니다.
RAW_DIR = OUTPUT_DIR / "raw"

# 전처리가 끝난 회원표를 저장할 하위 폴더입니다.
PROCESSED_DIR = OUTPUT_DIR / "processed"

# 히스토그램·박스플롯·PCA 그림을 저장할 하위 폴더입니다.
FIGURE_DIR = OUTPUT_DIR / "figures"

# SQLite DB 파일을 저장할 하위 폴더입니다.
DATABASE_DIR = OUTPUT_DIR / "database"

# 여기서는 폴더 주소를 나타내는 Path 객체만 준비합니다.
# 모듈을 import하는 순간 빈 폴더를 모두 만들지는 않습니다.
# 실제로 저장할 교시가 필요한 폴더에만 mkdir(parents=True, exist_ok=True)를 실행합니다.


def configure_plot_fonts() -> None:
    """운영체제에 맞는 한글 글꼴을 찾아 Matplotlib 그래프에 적용합니다."""

    # 그래프를 그리는 교시에서만 Matplotlib을 불러옵니다.
    # 그래서 API·DB 교시가 week3_common을 import해도 그래프 라이브러리까지
    # 불필요하게 준비하지 않습니다. import한 plt는 이 함수 안에서만 사용합니다.
    import matplotlib.pyplot as plt

    # Mac·Windows·일반 Linux 환경에서 자주 볼 수 있는 글꼴 이름을 후보로 정합니다.
    # candidate_font는 후보 list에서 한 번에 꺼낸 글꼴 이름을 담는 우리가 만든 변수입니다.
    for candidate_font in ["AppleGothic", "Malgun Gothic", "NanumGothic"]:

        # Matplotlib이 현재 컴퓨터에서 알고 있는 글꼴 목록에 후보가 있는지 검사합니다.
        # any()는 여러 비교 결과 중 하나라도 True이면 True를 반환하는 Python 내장 함수입니다.
        if any(font.name == candidate_font for font in plt.matplotlib.font_manager.fontManager.ttflist):

            # 찾은 글꼴을 이후 그래프의 기본 글꼴로 지정합니다.
            # rcParams는 Matplotlib의 전역 그래프 설정을 담은 딕셔너리와 비슷한 객체입니다.
            plt.rcParams["font.family"] = candidate_font

            # 첫 번째로 찾은 글꼴을 사용하고 후보 탐색을 끝냅니다.
            break

    # 음수 기호가 한글 글꼴에서 깨지지 않도록 마이너스 기호 표시 옵션을 끕니다.
    # 이 함수는 화면에 값을 반환하지 않고 Matplotlib 설정을 바꾸므로 반환값은 None입니다.
    plt.rcParams["axes.unicode_minus"] = False


def fallback_members(limit: int = 100):
    # API에 연결할 수 없을 때도 같은 화면·전처리 흐름을 연습할 수 있도록
    # 수업용 대체 CSV에서 회원 행을 읽어 반환합니다.
    # limit는 최대 몇 행을 사용할지 받는 우리가 정한 입력 변수이며 기본값은 100입니다.
    # 반환값은 CSV를 읽은 Pandas DataFrame입니다.

    # 이 함수가 실제로 호출될 때만 Pandas를 불러옵니다.
    import pandas as pd

    # DATA_DIR 아래의 대체 CSV 주소를 Path 객체로 만듭니다.
    # path는 파일을 읽기 위한 주소를 담는 함수 내부의 우리가 만든 변수입니다.
    path = DATA_DIR / "api_members_fallback.csv"

    # read_csv()는 path의 CSV를 DataFrame으로 읽습니다.
    # head(limit)는 위에서 정한 최대 행 수만 선택하고,
    # copy()는 그 선택 결과를 독립적인 DataFrame으로 만들어 반환합니다.
    return pd.read_csv(path).head(limit).copy()


def load_preprocessor():
    # 2주차에서 학습해 저장한 전처리기 객체를 다시 읽는 함수입니다.
    # 회원 데이터 자체가 아니라 결측치 대체값·범주 목록·스케일링 기준 등을 기억한
    # Python 객체를 반환합니다. 반환값을 담을 변수 이름은 호출하는 코드가 정합니다.

    # joblib은 Python 객체를 파일로 저장하고 다시 불러오는 라이브러리입니다.
    # 공통 파일을 import해도 이 함수를 호출할 때만 필요한 라이브러리를 준비합니다.
    import joblib

    # 미리 저장된 전처리기 파일의 위치를 Path 객체로 만듭니다.
    # path는 load_preprocessor 안에서만 쓰는 파일 주소 변수입니다.
    path = ARTIFACT_DIR / "matchmaking_preprocessor.joblib"

    # joblib.load()가 파일에 저장된 전처리기 객체를 메모리로 읽어 반환합니다.
    return joblib.load(path)


def transform_members(raw_df, preprocessor=None):
    # 원본 회원 DataFrame에 이미 학습된 전처리 규칙을 적용하는 함수입니다.
    # raw_df는 처리할 원본표, preprocessor는 저장된 전처리기 객체입니다.
    # preprocessor를 생략하면 아래에서 기본 joblib 파일을 자동으로 읽습니다.

    # 호출자가 전처리기를 따로 전달하지 않은 경우(None)에만 저장된 기본 객체를 불러옵니다.
    # None은 “아직 객체를 주지 않았다”는 Python 값입니다.
    if preprocessor is None:
        preprocessor = load_preprocessor()

    # 전처리기가 요구하는 열 이름이 원본표에 모두 있는지 먼저 검사합니다.
    # name은 INPUT_FEATURES에서 한 번에 꺼낸 열 이름이고,
    # missing_columns는 없는 열 이름만 모아 둔 우리가 만든 Python list입니다.
    missing_columns = [name for name in INPUT_FEATURES if name not in raw_df.columns]

    # 없는 열이 하나라도 있으면 빈 list가 아니므로 즉시 KeyError를 냅니다.
    # 조용히 잘못된 입력을 처리하지 않고, 어떤 열이 빠졌는지 오류 메시지로 알려 줍니다.
    if missing_columns:
        raise KeyError(f"전처리에 필요한 열이 없습니다: {missing_columns}")

    # raw_df[INPUT_FEATURES]는 원본표에서 필요한 13개 열을 INPUT_FEATURES list의
    # 순서대로 선택한 새 DataFrame입니다. ID나 정답 열은 여기에 포함하지 않습니다.
    # transform()은 새 데이터로 중앙값·범주·스케일 기준을 다시 학습하지 않고,
    # preprocessor가 이미 기억한 규칙을 적용한 결과를 반환합니다.
    return preprocessor.transform(raw_df[INPUT_FEATURES])


def timestamp_text(now: datetime | None = None) -> str:
    # 파일 이름·수집 ID에 사용할 날짜·시각 문자열을 만드는 함수입니다.
    # now는 테스트할 때 원하는 datetime을 넣을 수 있는 선택 입력이고,
    # 아무 값도 주지 않으면 현재 시각을 사용합니다.

    # now가 있으면 그것을, None이면 datetime.now()로 현재 시각을 current에 저장합니다.
    # current는 함수 안에서 사용할 현재 시각이라는 의미로 우리가 정한 변수명입니다.
    current = now or datetime.now()

    # datetime 객체의 strftime()으로 YYYYMMDD_HHMMSS 형식의 문자열을 반환합니다.
    # 예: 20261015_143005 -> 파일 이름이 서로 겹치지 않도록 구분하기 쉽습니다.
    return current.strftime("%Y%m%d_%H%M%S")


def add_collection_columns(processed_df, raw_df, collection_id: str):
    # 전처리 결과에 회원 식별 정보와 수집분 ID를 덧붙여 저장용 DataFrame을 만드는 함수입니다.
    # 목표는 숫자·원-핫 처리 결과만 남은 표에도 “어느 회원, 어느 지역·등급,
    # 어느 수집 시점의 데이터인가”를 추적할 수 있게 하는 것입니다.

    # 이 함수는 merge()로 두 표의 행을 member_id 기준으로 찾아 연결하지 않습니다.
    # processed_df와 raw_df의 행 순서가 같다는 전제에서,
    # 원본표의 식별 열을 처리 결과표에 새 열로 삽입합니다.
    #
    # 첫 번째 인수 processed_df: 전처리가 끝난 DataFrame
    # 두 번째 인수 raw_df: member_id와 원래의 회원 정보를 가진 원본 DataFrame
    # 세 번째 인수 collection_id: 이번 수집분을 구분하는 문자열
    # 처리 결과표를 원본과 분리해서 복사합니다.
    # result는 식별 열을 추가한 뒤 반환할 우리가 만든 DataFrame 변수입니다.
    result = processed_df.copy()

    # insert(위치, 열 이름, 열 값) 형식으로 원본표의 회원 등급을 새 열로 넣습니다.
    # 0은 맨 앞을 뜻하며, 현재 코드는 같은 위치에 계속 삽입하므로
    # 마지막에 넣은 collection_id가 최종적으로 가장 왼쪽에 옵니다.
    # reset_index(drop=True)는 원본 열의 행 번호를 0부터 다시 맞춰
    # 같은 위치의 처리 결과 행과 값이 대응하도록 합니다.
    result.insert(0, "membership_tier", raw_df["membership_tier"].reset_index(drop=True))

    # 원본표의 residence_region 열을 같은 행 순서로 앞에 삽입합니다.
    result.insert(0, "residence_region", raw_df["residence_region"].reset_index(drop=True))

    # 원본표의 member_id 열을 삽입해 처리 결과가 어느 회원의 것인지 남깁니다.
    result.insert(0, "member_id", raw_df["member_id"].reset_index(drop=True))

    # collection_id는 이번에 함께 받은 행 묶음을 구분하는 우리가 정한 문자열입니다.
    # 하나의 문자열 값을 insert에 주면 Pandas가 그 값을 모든 행에 반복해 넣습니다.
    result.insert(0, "collection_id", collection_id)

    # 원본 processed_df는 바뀌지 않고, 식별 열이 추가된 새 DataFrame을 반환합니다.
    return result


def open_sqlite(db_path: Path | None = None) -> sqlite3.Connection:
    # SQLite DB 파일에 연결하는 공통 함수입니다.
    # db_path를 주면 그 위치를 사용하고, 생략하면 3주차 기본 DB 위치를 사용합니다.
    # 반환값은 SQL 문장을 실행할 수 있는 sqlite3.Connection 객체입니다.

    # or는 db_path가 None이 아닐 때는 전달받은 경로를,
    # None일 때는 기본 파일 경로를 target에 저장합니다.
    # target은 실제로 열 DB 파일의 Path 객체라는 뜻으로 정한 변수명입니다.
    target = db_path or (DATABASE_DIR / "matchmaking_operations.db")

    # DB 파일을 만들기 전에 부모 폴더를 준비합니다.
    # parents=True는 database를 포함해 필요한 상위 폴더까지 만들고,
    # exist_ok=True는 이미 폴더가 있어도 오류를 내지 않게 합니다.
    target.parent.mkdir(parents=True, exist_ok=True)

    # connect()는 target 위치의 SQLite 파일을 열거나 없으면 새로 만들고,
    # Python 코드와 해당 DB 사이의 연결 객체를 반환합니다.
    return sqlite3.connect(target)


def make_pca_result(raw_df):
    # 원본 회원표를 PCA 두 축 결과표로 바꾸는 공통 함수입니다.
    # 목표는 9개의 숫자 열을 결측치 처리·스케일링한 뒤 PC1·PC2 두 좌표로 줄이고,
    # 그래프에서 회원을 구분할 ID와 등급을 결과표에 다시 붙이는 것입니다.
    # 반환값은 (결과 DataFrame, PCA 객체) 두 값을 묶은 tuple입니다.

    # PCA 계산에 필요한 라이브러리는 이 함수를 실제로 호출할 때만 불러옵니다.
    import pandas as pd
    from sklearn.decomposition import PCA
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler

    # raw_df에서 NUMERIC_FEATURES에 적은 숫자 열만 고릅니다.
    # SimpleImputer(strategy="median")는 열별 중앙값을 배우고 빈값을 채웁니다.
    # fit_transform() 결과 numeric_values는 결측치가 채워진 NumPy 배열입니다.
    numeric_values = SimpleImputer(strategy="median").fit_transform(raw_df[NUMERIC_FEATURES])

    # StandardScaler가 numeric_values의 열별 평균·표준편차를 배우고 크기를 맞춥니다.
    # scaled_values도 PCA에 넣을 NumPy 배열이며, 행 순서는 raw_df와 같습니다.
    scaled_values = StandardScaler().fit_transform(numeric_values)

    # PCA 객체를 만들고 결과를 두 개의 새 축으로 줄이도록 설정합니다.
    # pca는 PCA가 계산한 축과 설명 비율을 보관하는 우리가 만든 객체 변수입니다.
    pca = PCA(n_components=2, random_state=42)

    # fit_transform()은 scaled_values의 분산 구조를 학습하고
    # 각 회원을 PC1·PC2 두 좌표로 바꿉니다.
    # coordinates는 2열 NumPy 배열이며, 각 행은 원래 회원 한 명에 대응합니다.
    coordinates = pca.fit_transform(scaled_values)

    # 좌표 배열에는 열 이름이 없으므로 PC1·PC2 이름을 붙여 DataFrame으로 만듭니다.
    # index=raw_df.index는 원본표의 행 인덱스를 그대로 보존해 행 대응을 유지합니다.
    result = pd.DataFrame(coordinates, columns=["PC1", "PC2"], index=raw_df.index)

    # PCA에는 넣지 않은 member_id를 결과표 맨 앞에 붙여 회원을 추적할 수 있게 합니다.
    # .values는 Series의 값만 NumPy 배열로 꺼내 result의 행 순서에 맞춥니다.
    result.insert(0, "member_id", raw_df["member_id"].values)

    # membership_tier도 계산 입력은 아니지만 그래프 색상·그룹 비교에 필요하므로 붙입니다.
    result["membership_tier"] = raw_df["membership_tier"].values

    # 결과표와 PCA 객체를 함께 반환합니다.
    # 호출자는 result, pca = make_pca_result(raw_df)처럼 두 변수로 나눠 받을 수 있습니다.
    return result, pca


def make_activity_figure(raw_df):
    # 회원별 active_days 분포 히스토그램을 만드는 공통 함수입니다.
    # 그래프를 바로 화면에 띄우지 않고 Matplotlib Figure 객체를 반환하므로,
    # Streamlit에서는 st.pyplot(figure), 파일 저장에서는 figure.savefig()로 이어서 사용합니다.

    # 그래프를 만들 때만 Matplotlib을 불러옵니다.
    import matplotlib.pyplot as plt

    # 공통 한글 글꼴 설정을 먼저 적용합니다.
    configure_plot_fonts()

    # Figure 전체와 그 안에 그릴 Axes 공간을 한 번에 만듭니다.
    # figsize=(8, 4)는 가로·세로 크기(인치)이며 figure와 axes는 우리가 정한 변수명입니다.
    figure, axes = plt.subplots(figsize=(8, 4))

    # raw_df의 active_days Series를 10개 구간으로 나눠 회원 수 분포를 그립니다.
    # hist()는 axes에 그림을 그리는 Matplotlib 메서드이고,
    # color와 edgecolor는 막대 색과 막대 테두리 색을 정하는 설정입니다.
    axes.hist(raw_df["active_days"], bins=10, color="#2563EB", edgecolor="white")

    # 그래프가 무엇을 보여 주는지 제목과 두 축의 설명을 붙입니다.
    axes.set_title("회원의 30일 활동일 분포")
    axes.set_xlabel("로그인한 날짜 수")
    axes.set_ylabel("회원 수")

    # 제목·축 이름이 겹치거나 잘리지 않도록 Figure 안 여백을 자동으로 조정합니다.
    figure.tight_layout()

    # 완성한 Figure를 호출한 쪽으로 반환합니다. 이 함수 안에서는 화면 출력·파일 저장을 하지 않습니다.
    return figure
