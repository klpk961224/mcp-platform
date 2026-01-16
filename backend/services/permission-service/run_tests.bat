@echo off
REM 运行permission-service测试

echo ========================================
echo 运行permission-service测试
echo ========================================

cd /d %~dp0

echo.
echo [1/4] 运行单元测试...
pytest tests/unit/ -v --tb=short --cov=app --cov-report=term-missing --cov-report=html

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 单元测试失败！
    exit /b 1
)

echo.
echo [2/4] 运行集成测试...
pytest tests/integration/ -v --tb=short --cov=app --cov-append --cov-report=term-missing --cov-report=html

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 集成测试失败！
    exit /b 1
)

echo.
echo [3/4] 生成测试报告...
pytest tests/ -v --tb=short --cov=app --cov-append --cov-report=term-missing --cov-report=html:htmlcov

echo.
echo [4/4] 测试完成！
echo.
echo 测试报告已生成在 htmlcov/ 目录
echo ========================================

exit /b 0