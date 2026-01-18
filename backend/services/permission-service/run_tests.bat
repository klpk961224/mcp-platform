@echo off
REM 杩愯permission-service娴嬭瘯

echo ========================================
echo 杩愯permission-service娴嬭瘯
echo ========================================

cd /d %~dp0

echo.
echo [1/4] 杩愯鍗曞厓娴嬭瘯...
pytest tests/unit/ -v --tb=short --cov=app --cov-report=term-missing --cov-report=html

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 鍗曞厓娴嬭瘯澶辫触锛?    exit /b 1
)

echo.
echo [2/4] 杩愯闆嗘垚娴嬭瘯...
pytest tests/integration/ -v --tb=short --cov=app --cov-append --cov-report=term-missing --cov-report=html

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 闆嗘垚娴嬭瘯澶辫触锛?    exit /b 1
)

echo.
echo [3/4] 鐢熸垚娴嬭瘯鎶ュ憡...
pytest tests/ -v --tb=short --cov=app --cov-append --cov-report=term-missing --cov-report=html:htmlcov

echo.
echo [4/4] 娴嬭瘯瀹屾垚锛?echo.
echo 娴嬭瘯鎶ュ憡宸茬敓鎴愬湪 htmlcov/ 鐩綍
echo ========================================

exit /b 0
