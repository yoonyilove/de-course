# 2주차 학생 배포용 데이터

## 파일

- `members.csv`: 오류 없는 전체 회원 프로필 1,000행, 59열
- `preferences.csv`: 희망조건 1,000행, 17열. 2주차 필수 실습에서는 사용하지 않는 확장 자료
- `matches.csv`: 추천·응답·만남 이력 5,000행, 22열. 2주차 필수 실습에서는 사용하지 않는 확장 자료
- `activity_batches/`: 일별 활동 30,000행을 나눈 CSV 25개
- `00_2주차_데이터_열이름과뜻.md`: 수업에서 쓰는 열의 쉬운 설명
- `data_dictionary_week2.csv`, `2주차_데이터사전.xlsx`: 같은 내용을 표로 정리한 데이터 사전

## 핵심 실습

1. `glob`로 `activity_batch_*.csv` 25개를 찾습니다.
2. 각 파일을 반복해서 읽고 파일명을 나타내는 `source_file` 열을 붙입니다.
3. `pd.concat()`으로 30,000행을 합칩니다.
4. `pivot_table()`과 `melt()`로 긴 표와 넓은 표를 왕복합니다.
5. `members`의 필요한 열과 활동 집계를 `merge()`합니다.
6. 숫자 열의 `미측정`과 결측값을 Pipeline으로 처리합니다.

정상적으로 합치면 활동 로그는 정확히 30,000행입니다.

`stay_time_min`에는 숫자와 `미측정` 12개가 섞여 있습니다. Parquet 저장과 합계를 위해 `pd.to_numeric(errors="coerce")`로 정리합니다. `avg_reply_delay_sec`는 답장이 없던 날에는 비어 있는 것이 정상입니다.
