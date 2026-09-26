@echo off
REM Start React Frontend
REM =====================

echo ========================================
echo   Starting ML Analytics Frontend
echo ========================================
echo.

cd /d "%~dp0frontend"

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    echo This may take a few minutes...
    echo.
    call npm install
    echo.
)

echo Starting development server...
echo Frontend will open at: http://localhost:3000
echo.

npm run dev

pause
