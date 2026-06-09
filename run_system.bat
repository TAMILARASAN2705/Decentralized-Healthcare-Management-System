@echo off
REM Healthcare Management System Launcher
REM Python Backend - Version 2.0.0

echo === Healthcare Management System Launcher ===
echo Python Backend - Version 2.0.0
echo.
echo Choose an option:
echo 1. Run Backend (Console Interface)
echo 2. Run Web Server (Web Interface)
echo 3. Run Both (Backend + Web Server)
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting Python Backend...
    cd backend
    python main.py
) else if "%choice%"=="2" (
    echo.
    echo 🌐 Starting Web Server...
    cd web
    python server.py
) else if "%choice%"=="3" (
    echo.
    echo Starting both backend and web server...
    start "Healthcare Backend" python backend\main.py
    timeout /t 2 /nobreak >nul
    start "Healthcare Web Server" python web\server.py
    echo.
    echo ✅ Both servers are running!
    echo 🌐 Web Interface: http://localhost:8080
    echo 🖥️ Backend Console: Running in separate window
    echo.
    echo Press any key to stop servers...
    pause >nul
    taskkill /FI "WINDOWTITLE eq Healthcare Backend*" /F >nul 2>&1
    taskkill /FI "WINDOWTITLE eq Healthcare Web Server*" /F >nul 2>&1
    echo ✅ Servers stopped
) else if "%choice%"=="4" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Exiting...
    exit /b 1
)

pause
