# 3주차 9교시 선택 보충: 필터·지표·그래프·CSV 다운로드
# 코드는 VS Code/Cursor에서 수정하고, 실행은 VS Code/Cursor 터미널에서 합니다.
# 주피터 셀에서 이 Streamlit 앱을 실행하지 않습니다.

CURRENT_Q = 1
# 학생: Q1을 채우고 실행한 뒤, 다음 Q로 갈 때 이 숫자를 2, 3, 4, 5로 바꿉니다.
# 아래 st.stop()은 아직 풀지 않은 다음 Q 실행만 멈추는 제공 코드입니다.

from pathlib import Path
import platform

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# 제공 코드: 이 파일 위치를 기준으로 공통 데이터 파일의 주소를 만듭니다.
# parents[0]=9교시 폴더, [1]=week3, [2]=course_materials입니다.
COURSE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = COURSE_DIR / "matchmaking_data" / "03_week3" / "api_members_fallback.csv"

# 제공 코드: Mac/Windows의 한글 그래프 글꼴을 선택합니다.
plt.rcParams["font.family"] = "AppleGothic" if platform.system() == "Darwin" else "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="회원권별 활동 확인", layout="wide")
st.title("회원권별 활동 확인")
st.caption("회원권 등급을 선택하면 표·회원 수·그래프·다운로드 내용이 함께 바뀝니다.")
raw_members = pd.read_csv(DATA_PATH)


# Q1. 회원권 등급을 사용자가 직접 고르게 합니다
tier_options = ["전체", "베이직", "프리미엄", "VIP"]
selected_tier = st.___("회원권 등급", tier_options)
st.caption(f"선택한 등급: {selected_tier}")

# 제공 코드: Q2의 미완성 부분을 아직 실행하지 않습니다.
if CURRENT_Q == 1:
    st.stop()


# Q2. 선택한 회원권의 회원만 남깁니다
if selected_tier == "전체":
    filtered_members = raw_members.copy()
else:
    filtered_members = raw_members[
        raw_members["membership_tier"] == ___
    ].copy()

# 제공 코드: Q3의 미완성 부분을 아직 실행하지 않습니다.
if CURRENT_Q == 2:
    st.stop()


# Q3. 회원 수와 표가 같은 선택을 보여주게 합니다
st.metric("현재 회원 수", len(___))
st.metric("평균 활동일", round(filtered_members["active_days"].mean(), 1))
st.dataframe(___, hide_index=True)

# 제공 코드: Q4의 미완성 부분을 아직 실행하지 않습니다.
if CURRENT_Q == 3:
    st.stop()


# Q4. 선택한 회원들의 활동일 분포를 그립니다
figure, axes = plt.subplots(figsize=(8, 4))
axes.hist(___["active_days"], bins=10, range=(0, 30),
          color="#2563EB", edgecolor="white")
axes.set_title(f"{selected_tier} 회원의 30일 활동일 분포")
axes.set_xlabel("앱을 사용한 날짜 수")
axes.set_ylabel("회원 수")
st.pyplot(___)
plt.close(figure)

# 제공 코드: Q5의 미완성 부분을 아직 실행하지 않습니다.
if CURRENT_Q == 4:
    st.stop()


# Q5. 화면에서 보고 있는 회원표를 CSV로 내려받습니다
csv_bytes = filtered_members.to_csv(index=___).encode("utf-8-sig")
st.___(
    label="현재 표를 CSV로 다운로드",
    data=csv_bytes,
    file_name="filtered_members.csv",
    mime="text/csv"
)
