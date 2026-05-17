@echo off
echo ========================================
echo  MEDTRIAGE EXPERT SYSTEM - SETUP
echo ========================================
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install from https://www.python.org
    pause
    exit /b 1
)
echo [1/3] Installing dependencies...
pip install flask flask-cors --quiet
echo [2/3] Done.
echo [3/3] Starting server...
echo.
echo  >>> Open browser to: http://localhost:5000
echo  >>> Press Ctrl+C to stop
echo ========================================
python server.py
pause
