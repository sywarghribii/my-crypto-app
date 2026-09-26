@echo off
REM Start Complete ML Analytics Platform
REM ====================================

echo ========================================
echo   ML Analytics Platform
echo   Starting Backend and Frontend...
echo ========================================
echo.

REM Start Backend in new window
start "ML Analytics Backend" cmd /k "cd /d %~dp0backend && py -m uvicorn main:app --reload --host 127.0.0.1 --port 8001"

REM Wait a moment for backend to start
timeout /t 3 /nobreak > nul

REM Start Frontend in new window
start "ML Analytics Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo   Both servers are starting...
echo   Backend: http://localhost:8001/docs
echo   Frontend: http://localhost:3000
echo ========================================
echo.

pause
