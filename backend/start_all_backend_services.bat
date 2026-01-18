@echo off
chcp 65001 >nul
echo ========================================
echo 鍚姩浼佷笟绾I缁煎悎绠＄悊骞冲彴鎵€鏈夊悗绔湇鍔?echo ========================================
echo.

set PYTHONPATH=D:\WorkSpace\mcp-platform\backend

echo [1/6] 鍚姩璁よ瘉鍩熸湇鍔?(228001)...
start "璁よ瘉鍩熸湇鍔? cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\auth-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 228001"
timeout /t 3 /nobreak >nul

echo [2/6] 鍚姩鐢ㄦ埛鍩熸湇鍔?(228002)...
start "鐢ㄦ埛鍩熸湇鍔? cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\user-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 228002"
timeout /t 3 /nobreak >nul

echo [3/6] 鍚姩鏉冮檺鍩熸湇鍔?(228003)...
start "鏉冮檺鍩熸湇鍔? cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\permission-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 228003"
timeout /t 3 /nobreak >nul

echo [4/6] 鍚姩绯荤粺鍩熸湇鍔?(228004)...
start "绯荤粺鍩熸湇鍔? cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\system-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 228004"
timeout /t 3 /nobreak >nul

echo [5/6] 鍚姩鏀拺鍩熸湇鍔?(228005)...
start "鏀拺鍩熸湇鍔? cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\support-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 228005"
timeout /t 3 /nobreak >nul

echo [6/6] 鍚姩涓氬姟鍩熸湇鍔?(228006)...
start "涓氬姟鍩熸湇鍔? cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\business-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 228006"

echo.
echo ========================================
echo 鎵€鏈夋湇鍔″凡鍚姩锛?echo ========================================
echo.
echo 鏈嶅姟鍦板潃锛?echo - 璁よ瘉鍩熸湇鍔? http://localhost:228001
echo - 鐢ㄦ埛鍩熸湇鍔? http://localhost:228002
echo - 鏉冮檺鍩熸湇鍔? http://localhost:228003
echo - 绯荤粺鍩熸湇鍔? http://localhost:228004
echo - 鏀拺鍩熸湇鍔? http://localhost:228005
echo - 涓氬姟鍩熸湇鍔? http://localhost:228006
echo.
echo 鍋ュ悍妫€鏌ワ細
echo - http://localhost:228001/health
echo - http://localhost:228002/health
echo - http://localhost:228003/health
echo - http://localhost:228004/health
echo - http://localhost:228005/health
echo - http://localhost:228006/health
echo.
pause
