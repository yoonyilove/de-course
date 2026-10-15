from pathlib import Path

import pandas as pd
import requests
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
API_URL = "http://127.0.0.1:8010"
FALLBACK_PATH = BASE_DIR / "outputs" / "manufacturing_dashboard_ready.csv"


@st.cache_data(ttl=30)
def load_data():
    try:
        response = requests.get(
            API_URL + "/items",
            params={"limit": 240}, timeout=5
        )
        response.raise_for_status()
        return pd.DataFrame(response.json()), "API"
    except requests.RequestException:
        return pd.read_csv(FALLBACK_PATH), "CSV"


st.title("FILL_ME")
data, source_name = load_data()
st.caption(f"현재 데이터 출처: {source_name}")

segment_options = sorted(data["plant"].dropna().unique().tolist())
selected_segments = st.sidebar.FILL_ME(
    "공장 선택",
    options=segment_options,
    default=segment_options,
)
filtered = data[data["plant"].isin(selected_segments)].copy()

col1, col2, col3 = st.columns(3)
col1.FILL_ME("선택한 설비 수", len(filtered))
col2.FILL_ME("평균 30일 알람 수", round(filtered["alarm_count"].mean(), 2))
col3.FILL_ME("정비 확인 필요", int(filtered["maintenance_required"].sum()))

st.subheader("공장별 평균 30일 알람 수")
segment_chart = filtered.groupby("plant")["alarm_count"].mean().sort_values()
st.FILL_ME(segment_chart)

st.subheader("PCA 2차원 위치")
st.FILL_ME(filtered, x="pca_1", y="pca_2", color="status_label")

st.subheader("필터 결과")
st.FILL_ME(filtered, use_container_width=True)
csv_bytes = filtered.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "현재 표 CSV로 받기",
    data=csv_bytes,
    file_name="제조_filtered.csv",
    mime="text/csv",
)
