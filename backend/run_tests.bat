@echo off
chcp 65001 >nul
echo ========================================
echo 运行后端接口测试
echo ========================================
echo.

cd D:\WorkSpace\mcp-platform\backend\tests
set PYTHONPATH=D:\WorkSpace\mcp-platform\backend
python test_backend_apis.py

echo.
echo ========================================
echo 测试完成！
echo ========================================
echo.
echo 测试报告已生成：D:\WorkSpace\mcp-platform\backend\tests\测试报告.json
echo.
pause