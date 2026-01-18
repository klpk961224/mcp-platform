@echo off
chcp 65001 >nul
echo ========================================
echo 启动企业级AI综合管理平台所有后端服务
echo ========================================
echo.

set PYTHONPATH=D:\WorkSpace\mcp-platform\backend

echo [1/6] 启动认证域服务 (8001)...
start "认证域服务" cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\auth-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8001"
timeout /t 3 /nobreak >nul

echo [2/6] 启动用户域服务 (8002)...
start "用户域服务" cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\user-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8002"
timeout /t 3 /nobreak >nul

echo [3/6] 启动权限域服务 (8003)...
start "权限域服务" cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\permission-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8003"
timeout /t 3 /nobreak >nul

echo [4/6] 启动系统域服务 (8004)...
start "系统域服务" cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\system-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8004"
timeout /t 3 /nobreak >nul

echo [5/6] 启动支撑域服务 (8005)...
start "支撑域服务" cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\support-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8005"
timeout /t 3 /nobreak >nul

echo [6/6] 启动业务域服务 (8006)...
start "业务域服务" cmd /k "cd /d D:\WorkSpace\mcp-platform\backend\services\business-service && set PYTHONPATH=D:\WorkSpace\mcp-platform\backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8006"

echo.
echo ========================================
echo 所有服务已启动！
echo ========================================
echo.
echo 服务地址：
echo - 认证域服务: http://localhost:8001
echo - 用户域服务: http://localhost:8002
echo - 权限域服务: http://localhost:8003
echo - 系统域服务: http://localhost:8004
echo - 支撑域服务: http://localhost:8005
echo - 业务域服务: http://localhost:8006
echo.
echo 健康检查：
echo - http://localhost:8001/health
echo - http://localhost:8002/health
echo - http://localhost:8003/health
echo - http://localhost:8004/health
echo - http://localhost:8005/health
echo - http://localhost:8006/health
echo.
pause