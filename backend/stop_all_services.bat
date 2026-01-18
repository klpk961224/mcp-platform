@echo off
chcp 65001 >nul
echo ========================================
echo 鍋滄浼佷笟绾I缁煎悎绠＄悊骞冲彴Docker鏈嶅姟
echo ========================================

cd /d %~dp0

echo.
echo [1/2] 鍋滄鎵€鏈夋湇鍔?..
docker-compose down

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 璀﹀憡: 鏈嶅姟鍋滄澶辫触
    pause
    exit /b 1
)

echo.
echo [2/2] 娓呯悊鏁版嵁鍗?..
docker-compose down -v

echo.
echo ========================================
echo 鎵€鏈夋湇鍔″凡鍋滄锛?echo ========================================
echo.
echo 閲嶆柊鍚姩: start_all_services.bat
echo ========================================

pause
