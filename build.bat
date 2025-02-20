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
"%PYINSTALLER_PATH%" "%RTC_CLIENT_SCRIPT%" -w

REM 检查构建是否成功
if errorlevel 1 (
    echo ======Build failed!======
    pause
    exit /b 1
)

REM 定义 dist 目录路径
set "DIST_DIR=%SCRIPT_DIR%dist\rtc_client"

REM 检查 dist 目录是否存在
if not exist "%DIST_DIR%" (
    echo ======Error: dist directory not found at %DIST_DIR%======
    pause
    exit /b 1
)

REM 创建 logs 文件夹
echo ======Creating logs folder...======
mkdir "%DIST_DIR%\logs"

REM 检查 logs 文件夹是否创建成功
if not exist "%DIST_DIR%\logs" (
    echo ======Failed to create logs folder.======
)

REM 提示完成
echo ======Build completed!======
pause
