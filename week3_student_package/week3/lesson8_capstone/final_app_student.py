from pathlib import Path
import sys

HERE = Path(__file__).resolve()
WEEK3_DIR = HERE.parents[1]
if str(WEEK3_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK3_DIR))

from datetime import datetime
import joblib
import pandas as pd
import requests
import streamlit as st
from sqlalchemy import create_engine
from week3_common import (
    DATA_DIR, ARTIFACT_DIR, RAW_DIR, PROCESSED_DIR, DATABASE_DIR,
    INPUT_FEATURES, add_collection_columns,
    make_activity_figure, make_pca_result,
)

API_URL = "http://127.0.0.1:8000"
fallback_path = DATA_DIR / "api_members_fallback.csv"

# 이 앱이 실제로 저장하는 원본·처리·DB 폴더만 준비합니다.
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
artifact_path = ARTIFACT_DIR / "matchmaking_preprocessor.joblib"
engine = create_engine(
    f"sqlite:///{DATABASE_DIR / 'final_operations.db'}")

st.title("3주차 종합실습 · 회원 활동 운영 화면")

# Q1~Q2. API 또는 대체 CSV로 원본을 만들고 바로 저장
if st.button("1. 데이터 100명 준비하고 원본 저장"):
    try:
        response = requests.get(
            API_URL + "/members",
            params={"limit": 100}, timeout=5)
        response.raise_for_status()
        raw_members = pd.DataFrame(response.___())
        source_name = "API"
    except requests.RequestException:
        raw_members = pd.___(fallback_path)
        source_name = "대체 CSV"

    assert raw_members.shape == (100, 16)
    collection_id = datetime.now().strftime("___")
    raw_path = RAW_DIR / f"raw_final_{collection_id}.csv"
    raw_members.___(raw_path, index=___)
    assert raw_path.exists()

    st.session_state["raw_members"] = raw_members
    st.session_state["collection_id"] = collection_id
    st.session_state["source_name"] = source_name
    st.success(f"{source_name}에서 100명을 준비했습니다.")

has_raw = "raw_members" in st.session_state

# Q3. 저장 전처리기를 적용하고 처리 CSV 저장
if st.button("2. 저장된 기준으로 전처리하고 결과 저장",
             disabled=not has_raw):
    raw_members = st.session_state["raw_members"]
    preprocessor = joblib.___(artifact_path)
    new_X = raw_members[INPUT_FEATURES]
    processed_members = preprocessor.___(new_X)
    processed_path = PROCESSED_DIR / (
        f"processed_final_{st.session_state['collection_id']}.csv")
    processed_members.___(processed_path, index=___)
    assert processed_members.shape == (100, 36)
    assert processed_members.isna().sum().sum() == 0
    st.session_state["processed_members"] = processed_members
    st.success("회원 100명을 36개 처리 열로 바꿨습니다.")

has_processed = "processed_members" in st.session_state

# Q4. SQLite 저장 후 COUNT로 확인
if st.button("3. SQLite에 저장하고 행 수 확인",
             disabled=not has_processed):
    raw_members = st.session_state["raw_members"]
    processed_members = st.session_state["processed_members"]
    processed_for_db = add_collection_columns(
        processed_members, raw_members,
        st.session_state["collection_id"])
    processed_for_db.to_sql(
        "processed_members", engine,
        if_exists=___, index=False)
    row_count = pd.read_sql_query(
        "SELECT COUNT(*) AS row_count FROM processed_members",
        engine).loc[0, "row_count"]
    assert row_count == ___
    st.session_state["row_count"] = row_count
    st.success("SQLite에 100행을 저장했습니다.")

# Q5. 세 행 수, 그래프와 PCA 표시
st.subheader("완료 결과")
st.metric("원본 회원 수",
          len(st.session_state[___]) if has_raw else 0)
st.metric("처리 회원 수",
          len(st.session_state["processed_members"]) if has_processed else 0)
st.metric("DB 저장 행 수",
          st.session_state.get(___, 0))

if has_raw:
    raw_members = st.session_state["raw_members"]
    figure = make_activity_figure(raw_members)
    st.pyplot(figure)
    pca_result, pca = make_pca_result(raw_members)
    st.write(
        "PCA 두 축 설명력",
        round(pca.explained_variance_ratio_.sum() * 100, 1), "%")
    st.dataframe(pca_result.head())
else:
    st.info("1번 버튼부터 순서대로 실행해 주세요.")
