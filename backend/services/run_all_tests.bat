@echo off
REM 杩愯鎵€鏈夋湇鍔℃祴璇?
echo ========================================
echo 杩愯鎵€鏈夋湇鍔℃祴璇?echo ========================================

cd /d %~dp0

echo.
echo ========================================
echo [1/3] 杩愯auth-service娴嬭瘯
echo ========================================
cd auth-service
call run_tests.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo auth-service娴嬭瘯澶辫触锛?    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo [2/3] 杩愯user-service娴嬭瘯
echo ========================================
cd user-service
call run_tests.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo user-service娴嬭瘯澶辫触锛?    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo [3/3] 杩愯permission-service娴嬭瘯
echo ========================================
cd permission-service
call run_tests.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo permission-service娴嬭瘯澶辫触锛?    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo 鎵€鏈夋湇鍔℃祴璇曞畬鎴愶紒
echo ========================================

pause
exit /b 0
