# Surface Windows 완전 초보 환경설정

> **이번 학생용 배포본에서의 이름 안내**
> 이 폴더의 이름은 `week1_student_package`입니다. 환경 점검은 아래 명령으로 실행합니다.
> `python setup/02_1주차_환경점검.py`
> 아래 본문에 남아 있는 예전 배포본 이름은 참고용 예시입니다. 이 배포본에서는 지금 안내한
> 폴더명과 점검 파일을 사용합니다.

목표: 자동 점검에서 `SETUP CHECK: PASS`를 확인하고, 1주차 1교시 학생용 노트북을 `Python (de-course)` 커널로 열어 첫 준비 셀을 실행합니다.

Surface는 x64 모델과 ARM64 모델이 모두 있으므로, 첫 단계에서 반드시 확인합니다.

## 준비물

- 인터넷 연결
- 약 30~60분
- 저장 공간 10GB 이상
- 강의 패키지 ZIP 파일
- Windows 로그인 권한

## 1단계: Surface가 x64인지 ARM64인지 확인합니다

1. 화면 아래의 Windows 시작 버튼을 누릅니다.
2. 톱니바퀴 모양 `설정`을 누릅니다.
3. 왼쪽에서 `시스템`을 누릅니다.
4. 아래로 내려 `정보` 또는 `About`을 누릅니다.
5. `시스템 종류` 또는 `System type` 줄을 찾습니다.
6. 글자를 그대로 메모합니다.

### `x64 기반 프로세서`라고 보이는 경우

이 안내서를 계속 진행합니다.

### `ARM64 기반 프로세서`라고 보이는 경우

여기서 멈춥니다. 이 안내서는 x64 Surface에서 검증한 절차입니다. ARM64 모델은 설치 파일과 과학 패키지 호환성을 별도로 확인해야 하므로 강사에게 먼저 알립니다.

VS Code는 Windows Arm64용이 있지만, Python 과학 패키지까지 포함한 강의 환경은 별도 검증이 필요합니다.

## 2단계: Miniconda를 받습니다

1. Edge 또는 Chrome을 엽니다.
2. 주소창에 `https://docs.conda.io/miniconda.html`을 입력합니다.
3. Installation tap에서 Windows 설치 파일을 찾습니다. 
   https://www.anaconda.com/download/success?reg=skipped-miniconda
4. `Windows x86_64` 또는 `Windows 64-bit` 설치 파일을 선택합니다.
5. `.exe` 파일의 다운로드가 끝날 때까지 기다립니다.

정상 기준: 다운로드 폴더에 이름에 `Windows-x86_64`가 들어간 파일이 있습니다.

## 3단계: Miniconda를 설치합니다

1. 파일 탐색기를 엽니다.
2. 왼쪽에서 `다운로드`를 누릅니다.
3. Miniconda `.exe` 파일을 두 번 누릅니다.
4. Windows가 실행 여부를 물으면 게시자가 Anaconda인지 확인하고 진행합니다.
5. `Next`를 누릅니다.
6. 사용권 화면에서 `I Agree`를 누릅니다.
7. 설치 대상은 `Just Me`를 선택합니다.
8. 설치 폴더는 기본값을 그대로 둡니다.
9. 추가 옵션도 기본값을 사용합니다.
10. `Add Miniconda to PATH`가 기본적으로 선택되지 않았다면 억지로 선택하지 않습니다.
11. `Install`을 누릅니다.
12. 완료될 때까지 기다립니다.
13. `Finish`를 누릅니다.

## 4단계: PowerShell을 엽니다

Windows에 기본으로 들어 있는 PowerShell을 사용합니다. 별도의 Anaconda Prompt를 사용하지 않습니다.

1. Windows 시작 버튼을 누릅니다.
2. 검색창에 `PowerShell`을 입력합니다.
3. `Windows PowerShell` 또는 `PowerShell`을 누릅니다.
4. 파란색 또는 검은색 창이 열리면 마지막 줄을 한 번 클릭합니다.
5. 아래 명령을 실행합니다.

```bat
conda --version
```

이 명령의 뜻: “Miniconda가 설치되어 있고 이 명령창이 conda를 찾을 수 있다면 버전 번호를 보여줘.”

왜 필요한가: 환경을 만들기 전에 가장 작은 명령으로 설치와 명령창 연결을 확인합니다. `bat`라는 표시는 입력하지 않고 `conda --version`만 입력합니다.

정상 기준: `conda 26...`처럼 conda와 숫자가 보입니다.

PowerShell이 보이지 않으면 시작 메뉴의 `Windows 도구` 안에서 찾아 실행합니다.

`conda`를 찾을 수 없다는 메시지가 나오면 아래 명령을 한 번 실행합니다.

```powershell
conda init powershell
```

PowerShell 창을 닫았다가 새로 열고 `conda --version`을 다시 실행합니다.

## 5단계: 강의 ZIP을 풉니다

1. 파일 탐색기에서 강의 ZIP을 찾습니다.
2. ZIP을 마우스 오른쪽 버튼으로 누릅니다.
3. `압축 풀기` 또는 `Extract All...`을 누릅니다.
4. `압축 풀기` 버튼을 누릅니다.
5. 강사용 전체 자료라면 `course_materials`, 학생용 ZIP이라면 `week1_student_package` 폴더를 엽니다.
   GitHub에서 받은 ZIP은 바깥 폴더 이름에 저장소 이름과 `-main`이 붙을 수 있습니다. 이 경우에도
   안에 `week1`, `matchmaking_data`, `setup`, `requirements.txt`가 바로 보이는 폴더를 사용합니다.
6. 바로 안에 `week1`, `matchmaking_data`, `setup`, `requirements.txt`가 있는지 확인합니다.
7. 이 폴더 전체를 `문서` 폴더로 옮깁니다.

중요: ZIP 안에서 노트북을 직접 실행하지 않습니다. 반드시 `압축 풀기`를 먼저 합니다.

## 6단계: PowerShell을 강의 폴더로 이동합니다

1. 파일 탐색기에서 바로 안에 `week1`, `matchmaking_data`, `setup`이 있는 폴더를 엽니다.
2. 창 위쪽의 폴더 주소 부분을 한 번 누릅니다.
3. 전체 주소가 선택되면 `Ctrl+C`로 복사합니다.
4. PowerShell로 돌아갑니다.
5. 아래처럼 `Set-Location` 뒤에 공백을 입력합니다.
6. 복사한 주소를 큰따옴표 안에 붙여넣습니다.
7. 주소 앞뒤에 큰따옴표를 붙입니다.

예시:

```powershell
Set-Location "C:\Users\내이름\Documents\week1_student_package"
```

8. Enter를 누릅니다.
9. 아래 명령을 실행합니다.

```powershell
dir
```

이 명령의 뜻: 현재 명령창이 서 있는 폴더 안의 파일과 하위 폴더 목록을 보여줍니다.

왜 필요한가: `week1`, `matchmaking_data`, `setup`, `requirements.txt`가 보여야 다음 설치와 환경점검 명령이 파일을 찾을 수 있습니다.

정상 기준: 목록에 `week1`, `matchmaking_data`, `setup`, `requirements.txt`가 보입니다.

## 7단계: 수업 전용 환경을 만듭니다

아래 명령을 실행합니다. 몇 분 걸릴 수 있습니다.

```bat
conda create -n de-course python=3.12 -y
```

이 명령의 뜻: “`de-course`라는 강의 전용 공구함을 만들고 Python 3.12를 넣어줘. 확인 질문에는 yes로 진행해.”

왜 필요한가: Windows에 이미 다른 Python이 있더라도 강의 패키지와 섞이지 않게 분리합니다.

끝나면 다음 명령을 실행합니다.

```bat
conda activate de-course
```

이 명령의 뜻: “지금부터 `de-course` 안의 Python과 pip를 사용해.”

왜 필요한가: 환경을 만든 뒤 활성화해야 패키지가 올바른 위치에 설치됩니다. 성공 표시는 입력 줄 앞의 `(de-course)`입니다.

정상 기준: 검은 창의 마지막 줄 맨 앞에 `(de-course)`가 보입니다.

## 8단계: 수업 패키지를 설치합니다

앞에 `(de-course)`가 보이는지 먼저 확인합니다.

```bat
python -m pip install -r requirements.txt
```

이 명령의 뜻: “현재 Python으로 pip를 실행해 지금 폴더의 `requirements.txt`에 적힌 패키지를 전부 설치해.”

왜 필요한가: 1·2·3주차에 필요한 도구를 같은 목록으로 설치합니다. `python -m pip`는 현재 활성화한 Python에 설치하라는 뜻을 분명하게 합니다.

5~20분 정도 걸릴 수 있습니다. 글자가 많이 움직이는 것은 정상입니다.

정상 기준:

- 마지막 부분에 빨간색 `ERROR`가 없습니다.
- 다시 `(de-course)` 입력 줄이 나타납니다.

## 9단계: 노트북용 커널을 등록합니다

```bat
python -m ipykernel install --user --name de-course --display-name "Python (de-course)"
```

이 명령의 뜻: VS Code의 노트북 커널 목록에 현재 환경을 `Python (de-course)`라는 화면 이름으로 등록합니다.

왜 필요한가: 터미널에서 환경을 만들었어도 VS Code가 노트북 실행기로 바로 표시하지 못할 수 있기 때문입니다.

정상 기준: `Installed kernelspec de-course`와 비슷한 문장이 보입니다.

## 10단계: 자동 상태 검사를 실행합니다

```powershell
python setup\02_1주차_환경점검.py
```

이 명령의 뜻: Python 버전, 환경 위치, 패키지, 데이터와 노트북 파일을 읽기 전용으로 검사합니다.

왜 필요한가: 설치 전체를 다시 하지 않고 FAIL 항목만 찾아 고치기 위해서입니다.

정상 기준:

```text
SETUP CHECK: PASS
```

## 11단계: VS Code를 설치합니다

1. 브라우저에서 `https://code.visualstudio.com/Download`를 엽니다.
2. Windows `User Installer`의 `x64`를 선택합니다.
3. Surface가 ARM64라면 VS Code 자체는 `Arm64`를 선택하지만, 이 안내의 Miniconda 과정은 진행하지 않습니다.
4. 받은 설치 파일을 두 번 누릅니다.
5. 사용권에 동의합니다.
6. 설치 위치는 기본값을 사용합니다.
7. 시작 메뉴 폴더도 기본값을 사용합니다.
8. `PATH에 추가`가 보이면 기본 선택을 유지합니다.
9. `설치`를 누릅니다.
10. 완료 후 VS Code를 실행합니다.

## 12단계: Python과 Jupyter 확장을 설치합니다

1. VS Code 왼쪽의 네모 블록 모양 `Extensions`를 누릅니다.
2. `Python`을 검색합니다.
3. 게시자가 `Microsoft`인 Python을 설치합니다.
4. `Jupyter`를 검색합니다.
5. 게시자가 `Microsoft`인 Jupyter를 설치합니다.

정상 기준: 두 확장의 버튼이 `Uninstall` 또는 `Disable`로 보입니다.

## 13단계: 강의 폴더를 엽니다

1. VS Code 위 메뉴에서 `File`을 누릅니다.
2. `Open Folder...`를 누릅니다.
3. 바로 안에 `week1`, `matchmaking_data`, `setup`이 있는 폴더를 선택합니다.
4. `Select Folder`를 누릅니다.
5. 신뢰 여부를 물으면 본인이 받은 강의자료인지 확인하고 신뢰합니다.

정상 기준: 왼쪽 파일 목록에 `week1`, `matchmaking_data`, `setup`이 보입니다.

## 14단계: 1주차 1교시 학생용 노트북과 커널을 선택합니다

1. 왼쪽에서 `week1`을 펼칩니다.
2. `1주차_1교시_학생용_지적실험노트.ipynb`를 누릅니다. 파일이 바로 보이지 않으면 `lesson1_list_type_flow` 폴더 안을 봅니다.
3. 오른쪽 위의 `Select Kernel`을 누릅니다.
4. `Python Environments...`를 누릅니다.
5. `Python (de-course)`를 선택합니다.

정상 기준: 오른쪽 위 커널 이름에 `de-course`가 보입니다.

## 15단계: 첫 준비 셀을 실행합니다

1. 첫 번째 Python 코드 셀의 왼쪽 삼각형 실행 버튼을 누릅니다. 처음부터 `Run All`을 누르지 않습니다.
2. 코드 셀 왼쪽에 `[1]`처럼 실행 순서가 표시될 때까지 기다립니다.
3. 빨간 오류 없이 준비된 회원 수나 첫 회원 정보가 출력되는지 확인합니다.

최종 정상 기준: 오른쪽 위 커널에 `de-course`가 보이고, 첫 준비 셀이 빨간 오류 없이 실행됩니다.

## 다음 날 다시 시작하는 방법

1. VS Code를 엽니다.
2. 최근 강의 폴더를 엽니다.
3. 노트북 오른쪽 위 커널이 `Python (de-course)`인지 봅니다.
4. 터미널 명령이 필요하면 PowerShell을 열고 `conda activate de-course`부터 실행합니다.
