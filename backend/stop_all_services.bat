@echo off
chcp 65001 >nul
echo ========================================
echo 停止企业级AI综合管理平台Docker服务
echo ========================================

cd /d %~dp0

echo.
echo [1/2] 停止所有服务...
docker-compose down

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 警告: 服务停止失败
    pause
    exit /b 1
)

echo.
echo [2/2] 清理数据卷...
docker-compose down -v

echo.
echo ========================================
echo 所有服务已停止！
echo ========================================
echo.
echo 重新启动: start_all_services.bat
echo ========================================

pause