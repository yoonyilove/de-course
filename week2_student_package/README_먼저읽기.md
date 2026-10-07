# 2주차 학생용 먼저 읽기

## 가장 먼저 기억할 한 문장

> 압축을 푼 뒤 파일을 따로 옮기지 말고, 압축을 풀어서 생긴 최상위 폴더 전체를 VS Code에서 엽니다.

2주차 노트북은 데이터 폴더의 위치를 자동으로 찾습니다. 노트북이나 CSV 파일을 다른 폴더로 따로 옮기면 서로의 위치 관계가 끊어져 데이터를 찾지 못할 수 있습니다.

## 강사에게 받는 파일

강사는 수업 전에 `week2_student_package.zip` 파일 하나를 제공합니다.

이 압축파일에는 다음 자료가 함께 들어 있습니다.

- 교시별 학생용 노트북
- 2주차 회원 데이터
- `activity_batches` 폴더
- `activity_batch_01.csv`부터 `activity_batch_25.csv`까지의 활동 기록 파일

`activity_batches`는 학생이 새로 만드는 폴더가 아닙니다. 압축파일 안에 이미 들어 있습니다.

## 1단계: 압축파일을 찾기 쉬운 곳으로 옮깁니다

다운로드한 `week2_student_package.zip`을 문서 폴더처럼 찾기 쉬운 곳으로 옮깁니다.

- Mac 예시: `문서`
- Windows 예시: `문서`

다운로드 폴더에서 작업해도 실행은 가능하지만, 다른 파일과 섞여 수업자료를 찾기 어려울 수 있습니다.

## 2단계: 압축을 한 번 풉니다

### Mac

1. Finder에서 `week2_student_package.zip`을 찾습니다.
2. ZIP 파일을 두 번 클릭합니다.
3. 같은 위치에 `week2_student_package` 폴더가 생기는지 확인합니다.

### Windows

1. 파일 탐색기에서 `week2_student_package.zip`을 찾습니다.
2. ZIP 파일을 마우스 오른쪽 버튼으로 클릭합니다.
3. `모두 압축 풀기`를 선택합니다.
4. 압축을 풀어서 생긴 `week2_student_package` 폴더를 확인합니다.

ZIP 파일 안을 직접 열어 노트북을 실행하지 않습니다. 반드시 압축을 먼저 풉니다.

## 3단계: 폴더 구조를 확인합니다

압축을 풀면 다음과 비슷한 구조가 보여야 합니다.

```text
week2_student_package/
├── week2/
│   ├── 00_학생용_먼저읽기_압축해제와VSCode열기.md
│   ├── lesson1_find_files/
│   ├── lesson2_concat_sources/
│   ├── lesson3_reshape_export/
│   ├── lesson4_member_summary/
│   ├── lesson5_pipeline_build/
│   ├── lesson6_pipeline_save/
│   ├── lesson7_fastapi/
│   └── lesson8_capstone/
└── matchmaking_data/
    └── 02_week2/
        ├── members.csv
        └── activity_batches/
            ├── activity_batch_01.csv
            ├── activity_batch_02.csv
            ├── ...
            └── activity_batch_25.csv
```

폴더 구조의 모양이 중요한 이유는 노트북이 이 위치 관계를 이용해 데이터를 자동으로 찾기 때문입니다.

## 4단계: 최상위 폴더 전체를 VS Code에서 엽니다

1. VS Code를 실행합니다.
2. 상단 메뉴에서 `File` → `Open Folder`를 선택합니다.
3. 압축을 풀어서 생긴 `week2_student_package` 폴더를 선택합니다.
4. `열기`를 누릅니다.

`lesson1_find_files` 폴더만 여는 것이 아닙니다. 그 위에 있는 `week2_student_package` 폴더 전체를 엽니다.

## 5단계: 오늘 교시의 노트북 하나만 엽니다

1교시에는 다음 파일만 엽니다.

```text
week2/
└── lesson1_find_files/
    └── 2주차_1교시_학생용_지적실험노트.ipynb
```

파일 이름에 `강사용`, `전체실행`, `복습완성본`이 들어간 파일은 수업 시작 때 열지 않습니다.

## 6단계: 커널을 확인합니다

노트북 오른쪽 위의 커널 이름을 확인합니다.

```text
Python (de-course)
```

다른 이름이 보이면 커널 이름을 눌러 `Python (de-course)`를 선택합니다.

## `activity_batches`는 언제 만들어졌나요?

이 폴더는 강사가 수업 데이터를 준비할 때 미리 만든 폴더입니다. 회원 활동 기록 30,000행을 CSV 25개로 나누어 넣어 두었습니다.

학생은 이 폴더를 만들거나 CSV 25개를 직접 옮기지 않습니다.

1교시 Q1에서는 이미 받은 폴더의 위치가 맞는지만 확인합니다.

```python
batch_dir = DATA_DIR / "activity_batches"
print(batch_dir)
print(batch_dir.exists())
```

정상이라면 첫 출력은 `activity_batches`로 끝나는 폴더 주소이고, 두 번째 출력은 `True`입니다.

## 하면 안 되는 행동

- ZIP 파일의 압축을 풀지 않고 그 안에서 노트북을 바로 열지 않습니다.
- 학생용 노트북만 다운로드 폴더로 따로 옮기지 않습니다.
- `activity_batches` 안의 CSV 파일을 교시 폴더로 옮기지 않습니다.
- 폴더 이름 `activity_batches`를 한글이나 다른 이름으로 바꾸지 않습니다.
- `matchmaking_data`, `02_week2`, `week2` 폴더의 위치 관계를 바꾸지 않습니다.

## 문제가 생겼을 때

### `02_week2 데이터 폴더를 찾지 못했습니다`가 나온 경우

노트북만 따로 옮겼거나 VS Code에서 너무 안쪽 폴더만 열었을 가능성이 큽니다.

1. VS Code의 현재 창을 닫습니다.
2. `File` → `Open Folder`를 다시 선택합니다.
3. 압축을 풀어서 생긴 최상위 `week2_student_package` 폴더를 엽니다.
4. 학생용 노트북을 다시 열고 첫 셀부터 실행합니다.

### `batch_dir.exists()`가 `False`인 경우

다음 폴더가 실제로 있는지 확인합니다.

```text
matchmaking_data/02_week2/activity_batches
```

폴더가 없다면 압축이 완전히 풀리지 않았거나 자료 일부만 이동한 것입니다. ZIP을 새 폴더에 다시 풀어 최상위 폴더 전체를 엽니다.

## 수업이 끝날 때

자신이 빈칸을 채운 노트북을 같은 위치에 저장합니다. 파일을 다른 폴더로 옮길 필요는 없습니다.
