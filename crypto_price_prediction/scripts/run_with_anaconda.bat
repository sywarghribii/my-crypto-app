@echo off
REM ============================================================================
REM Daily Crypto Prediction - Using Anaconda Python
REM ============================================================================

echo ========================================
echo Daily Crypto Prediction Update
echo ========================================
echo.

cd /d "%~dp0"

REM Try using anaconda python directly
"C:\Users\Aloulou\anaconda3\python.exe" daily_update.py

if %ERRORLEVEL% NEQ 0 (
    echo Error: Python execution failed
    echo Please check that Anaconda is installed at C:\Users\Aloulou\anaconda3\
    pause
    exit /b 1
)

pause
