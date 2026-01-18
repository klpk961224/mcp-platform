@echo off
REM 运行所有服务测试

echo ========================================
echo 运行所有服务测试
echo ========================================

cd /d %~dp0

echo.
echo ========================================
echo [1/3] 运行auth-service测试
echo ========================================
cd auth-service
call run_tests.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo auth-service测试失败！
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo [2/3] 运行user-service测试
echo ========================================
cd user-service
call run_tests.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo user-service测试失败！
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo [3/3] 运行permission-service测试
echo ========================================
cd permission-service
call run_tests.bat
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo permission-service测试失败！
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo 所有服务测试完成！
echo ========================================

pause
exit /b 0