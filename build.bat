@echo off
REM 获取当前脚本所在的目录
set "SCRIPT_DIR=%~dp0"

REM 定义相对路径
set "PYINSTALLER_PATH=%SCRIPT_DIR%.venv\Scripts\pyinstaller.exe"
set "RTC_CLIENT_SCRIPT=%SCRIPT_DIR%rtc_client.py"

REM 检查 pyinstaller.exe 是否存在
if not exist "%PYINSTALLER_PATH%" (
    echo ======Error: pyinstaller.exe not found at %PYINSTALLER_PATH%======
    pause
    exit /b 1
)

REM 检查 rtc_client.py 是否存在
if not exist "%RTC_CLIENT_SCRIPT%" (
    echo ======Error: rtc_client.py not found at %RTC_CLIENT_SCRIPT%======
    pause
    exit /b 1
)

REM 运行 pyinstaller 命令
echo ======Running pyinstaller...======
"%PYINSTALLER_PATH%" "%RTC_CLIENT_SCRIPT%" --hide-console hide-early

REM 检查构建是否成功
if errorlevel 1 (
    echo ======Build failed!======
    pause
    exit /b 1
)

REM 提示完成
echo ======Build completed!======
pause
