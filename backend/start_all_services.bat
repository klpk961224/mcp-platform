@echo off
chcp 65001 >nul
echo ========================================
echo 启动企业级AI综合管理平台Docker服务
echo ========================================

cd /d %~dp0

echo.
echo [1/3] 检查Docker是否已安装...
docker --version
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 错误: 未检测到Docker，请先安装Docker
    pause
    exit /b 1
)

echo.
echo [2/3] 检查MySQL和Redis是否已启动...
echo 检查MySQL (localhost:3306)...
netstat -ano | findstr "3306" >nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 警告: MySQL未启动或端口3306不可访问
    echo 请确保MySQL已启动并监听在3306端口
    pause
    exit /b 1
)
echo MySQL已启动

echo 检查Redis (localhost:6379)...
netstat -ano | findstr "6379" >nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 警告: Redis未启动或端口6379不可访问
    echo 请确保Redis已启动并监听在6379端口
    pause
    exit /b 1
)
echo Redis已启动

echo.
echo [3/3] 启动所有服务...
docker-compose up -d --build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 错误: 服务启动失败
    pause
    exit /b 1
)

echo.
echo 等待服务启动...
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo 所有服务已启动！
echo ========================================
echo.
echo 服务地址（所有服务都在宿主机IP上）：
echo   - 认证服务: http://localhost:28001
echo   - 用户服务: http://localhost:28002
echo   - 权限服务: http://localhost:28003
echo   - 系统服务: http://localhost:28004
echo   - 支撑服务: http://localhost:28005
echo   - 业务服务: http://localhost:28006
echo.
echo 健康检查：
echo   - http://localhost:28001/health
echo   - http://localhost:28002/health
echo   - http://localhost:28003/health
echo   - http://localhost:28004/health
echo   - http://localhost:28005/health
echo   - http://localhost:28006/health
echo.
echo 查看日志: docker-compose logs -f
echo 查看状态: docker-compose ps
echo 停止服务: stop_all_services.bat
echo.
echo 详细文档: DOCKER_LOCAL_DEPLOYMENT.md
echo ========================================

pause