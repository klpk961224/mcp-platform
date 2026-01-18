@echo off
chcp 65001 >nul
echo ========================================
echo 鍚姩浼佷笟绾I缁煎悎绠＄悊骞冲彴Docker鏈嶅姟
echo ========================================

cd /d %~dp0

echo.
echo [1/3] 妫€鏌ocker鏄惁宸插畨瑁?..
docker --version
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 閿欒: 鏈娴嬪埌Docker锛岃鍏堝畨瑁匘ocker
    pause
    exit /b 1
)

echo.
echo [2/3] 妫€鏌ySQL鍜孯edis鏄惁宸插惎鍔?..
echo 妫€鏌ySQL (localhost:3306)...
netstat -ano | findstr "3306" >nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 璀﹀憡: MySQL鏈惎鍔ㄦ垨绔彛3306涓嶅彲璁块棶
    echo 璇风‘淇滿ySQL宸插惎鍔ㄥ苟鐩戝惉鍦?306绔彛
    pause
    exit /b 1
)
echo MySQL宸插惎鍔?
echo 妫€鏌edis (localhost:6379)...
netstat -ano | findstr "6379" >nul
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 璀﹀憡: Redis鏈惎鍔ㄦ垨绔彛6379涓嶅彲璁块棶
    echo 璇风‘淇漅edis宸插惎鍔ㄥ苟鐩戝惉鍦?379绔彛
    pause
    exit /b 1
)
echo Redis宸插惎鍔?
echo.
echo [3/3] 鍚姩鎵€鏈夋湇鍔?..
docker-compose up -d --build

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo 閿欒: 鏈嶅姟鍚姩澶辫触
    pause
    exit /b 1
)

echo.
echo 绛夊緟鏈嶅姟鍚姩...
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo 鎵€鏈夋湇鍔″凡鍚姩锛?echo ========================================
echo.
echo 鏈嶅姟鍦板潃锛堟墍鏈夋湇鍔￠兘鍦ㄥ涓绘満IP涓婏級锛?echo   - 璁よ瘉鏈嶅姟: http://localhost:228001
echo   - 鐢ㄦ埛鏈嶅姟: http://localhost:228002
echo   - 鏉冮檺鏈嶅姟: http://localhost:228003
echo   - 绯荤粺鏈嶅姟: http://localhost:228004
echo   - 鏀拺鏈嶅姟: http://localhost:228005
echo   - 涓氬姟鏈嶅姟: http://localhost:228006
echo.
echo 鍋ュ悍妫€鏌ワ細
echo   - http://localhost:228001/health
echo   - http://localhost:228002/health
echo   - http://localhost:228003/health
echo   - http://localhost:228004/health
echo   - http://localhost:228005/health
echo   - http://localhost:228006/health
echo.
echo 鏌ョ湅鏃ュ織: docker-compose logs -f
echo 鏌ョ湅鐘舵€? docker-compose ps
echo 鍋滄鏈嶅姟: stop_all_services.bat
echo.
echo 璇︾粏鏂囨。: DOCKER_LOCAL_DEPLOYMENT.md
echo ========================================

pause
