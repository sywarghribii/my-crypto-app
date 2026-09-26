@echo off
REM Start FastAPI Backend Server
REM =============================

echo Starting ML Analytics API...
echo.

cd /d "%~dp0backend"

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo No virtual environment found. Using system Python.
    echo To create one: python -m venv venv
    echo.
)

REM Start server
echo.
echo =====================================
echo   ML Analytics API Server
echo   URL: http://localhost:8001
echo   Docs: http://localhost:8001/docs
echo =====================================
echo.

py -m uvicorn main:app --reload --host 127.0.0.1 --port 8001

pause
