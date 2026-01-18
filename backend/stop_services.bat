@echo off
chcp 65001 >nul
echo ========================================
echo 停止企业级AI综合管理平台后端服务
echo ========================================
echo.

taskkill /F /FI "WINDOWTITLE eq 认证域服务*" 2>nul
taskkill /F /FI "WINDOWTITLE eq 用户域服务*" 2>nul
taskkill /F /FI "WINDOWTITLE eq 权限域服务*" 2>nul
taskkill /F /FI "WINDOWTITLE eq 系统域服务*" 2>nul
taskkill /F /FI "WINDOWTITLE eq 支撑域服务*" 2>nul
taskkill /F /FI "WINDOWTITLE eq 业务域服务*" 2>nul

echo.
echo ========================================
echo 所有服务已停止！
echo ========================================
echo.
pause