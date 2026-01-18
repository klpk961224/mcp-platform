@echo off
chcp 65001 >nul
echo ========================================
echo 杩愯鍚庣鎺ュ彛娴嬭瘯
echo ========================================
echo.

cd D:\WorkSpace\mcp-platform\backend\tests
set PYTHONPATH=D:\WorkSpace\mcp-platform\backend
python test_backend_apis.py

echo.
echo ========================================
echo 娴嬭瘯瀹屾垚锛?echo ========================================
echo.
echo 娴嬭瘯鎶ュ憡宸茬敓鎴愶細D:\WorkSpace\mcp-platform\backend\tests\娴嬭瘯鎶ュ憡.json
echo.
pause
