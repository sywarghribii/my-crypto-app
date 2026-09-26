@echo off
REM ============================================================================
REM Daily Crypto Prediction Automation Script
REM ============================================================================
REM This batch file runs the daily crypto prediction script
REM Can be scheduled with Windows Task Scheduler

echo ========================================
echo Daily Crypto Prediction Update
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "..\\.venv\\Scripts\\activate.bat" (
    echo Activating virtual environment...
    call "..\\.venv\\Scripts\\activate.bat"
    python daily_update.py
) else (
    REM Use system Python
    python daily_update.py
)

REM Pause to see results (remove this line when scheduling)
pause
