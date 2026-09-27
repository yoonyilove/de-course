@echo off
chcp 65001 >nul
setlocal
set "COURSE_ROOT=%~dp0.."

where conda >nul 2>nul
if errorlevel 1 (
  if exist "%USERPROFILE%\miniconda3\Scripts\activate.bat" (
    call "%USERPROFILE%\miniconda3\Scripts\activate.bat"
  ) else if exist "%USERPROFILE%\anaconda3\Scripts\activate.bat" (
    call "%USERPROFILE%\anaconda3\Scripts\activate.bat"
  ) else (
    echo [STOP] Miniconda를 찾지 못했습니다.
    echo setup\01_Surface_Windows_완전초보_설정.md의 2~4단계를 먼저 진행하세요.
    pause
    exit /b 1
  )
)

echo [1/4] de-course 환경을 만듭니다.
call conda env list > "%TEMP%\de_course_envs.txt"
findstr /B /C:"de-course " "%TEMP%\de_course_envs.txt" >nul
if errorlevel 1 (
  call conda create -n de-course python=3.12 -y
  if errorlevel 1 goto :failed
)

echo [2/4] de-course 환경을 엽니다.
call conda activate de-course
if errorlevel 1 goto :failed

echo [3/4] 3주 수업 패키지를 설치합니다. 시간이 걸릴 수 있습니다.
python -m pip install -r "%COURSE_ROOT%\requirements.txt"
if errorlevel 1 goto :failed

echo [4/4] Jupyter 커널을 등록하고 상태를 확인합니다.
python -m ipykernel install --user --name de-course --display-name "Python (de-course)"
if errorlevel 1 goto :failed
python "%COURSE_ROOT%\setup\02_1주차_환경점검.py"
if errorlevel 1 goto :failed

echo 완료되었습니다. 환경 점검 항목이 모두 PASS인지 확인하세요.
pause
exit /b 0

:failed
echo 설정 도중 멈췄습니다. 마지막 ERROR 줄을 사진으로 남기세요.
pause
exit /b 1
