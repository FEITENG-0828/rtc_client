@echo off
REM 获取当前脚本所在的目录
set "SCRIPT_DIR=%~dp0"

echo ======Start cleaning...======

REM 删除 build 目录
if exist "%SCRIPT_DIR%build" (
    echo Deleting build directory...
    rmdir /s /q "%SCRIPT_DIR%build"
    echo Build directory deleted.
) else (
    echo Build directory does not exist.
)

REM 删除 dist 目录
if exist "%SCRIPT_DIR%dist" (
    echo Deleting dist directory...
    rmdir /s /q "%SCRIPT_DIR%dist"
    echo Dist directory deleted.
) else (
    echo Dist directory does not exist.
)

REM 删除 rtc_client.spec 文件
if exist "%SCRIPT_DIR%rtc_client.spec" (
    echo Deleting rtc_client.spec file...
    del /q "%SCRIPT_DIR%rtc_client.spec"
    echo rtc_client.spec file deleted.
) else (
    echo rtc_client.spec file does not exist.
)

REM 删除 logs/rtc_client.log 文件
if exist "%SCRIPT_DIR%logs\rtc_client.log" (
    echo Deleting logs/rtc_client.log file...
    del /q "%SCRIPT_DIR%logs\rtc_client.log"
    echo logs/rtc_client.log file deleted.
) else (
    echo logs/rtc_client.log file does not exist.
)

REM 提示完成
echo ======Clean completed!======
pause
