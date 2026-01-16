@echo off
REM ??????

echo ========================================
echo ?????AI??????
echo ========================================

cd /d %~dp0

echo.
echo [1/2] ??????...
docker-compose down

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ??????????
    pause
    exit /b 1
)

echo.
echo [2/2] ????...
docker-compose down -v

echo.
echo ========================================
echo ??????
echo ========================================
echo.
echo ?????start_all_services.bat
echo ========================================

pause
