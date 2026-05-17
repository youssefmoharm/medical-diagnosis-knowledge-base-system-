@echo off
REM Medical Diagnosis KBS - Windows Deployment Helper

echo ==================================
echo Medical Diagnosis KBS Deployment
echo ==================================
echo.
echo Select deployment option:
echo 1) Local Development Server
echo 2) ngrok (Quick Share)
echo 3) Heroku (Cloud)
echo 4) Docker (Containerized)
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    echo Starting Local Development Server...
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
    echo Server starting on http://localhost:5000
    python server.py
    
) else if "%choice%"=="2" (
    echo.
    echo Setting up ngrok...
    echo.
    echo Prerequisites:
    echo - Download ngrok from https://ngrok.com/download
    echo - Extract to a folder in your PATH
    echo.
    echo Step 1: Start the Flask app in PowerShell/CMD
    echo - Run: python server.py
    echo.
    echo Step 2: In another terminal, expose with ngrok
    echo - Run: ngrok http 5000
    echo.
    echo Step 3: Share the provided public URL!
    pause
    
) else if "%choice%"=="3" (
    echo.
    echo Heroku Deployment
    echo ==================================
    echo.
    echo Prerequisites:
    echo - Install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
    echo - Have a GitHub account
    echo.
    echo Steps:
    echo 1. heroku login
    echo 2. heroku create your-app-name
    echo 3. git push heroku main
    echo.
    echo Your app will be at: https://your-app-name.herokuapp.com
    pause
    
) else if "%choice%"=="4" (
    echo.
    echo Docker Deployment
    echo ==================================
    echo.
    echo Prerequisites:
    echo - Install Docker from https://www.docker.com/products/docker-desktop
    echo.
    echo Building Docker image...
    docker build -t medical-kbs .
    
    echo.
    echo Running locally...
    docker run -p 5000:5000 medical-kbs
    
) else (
    echo Invalid choice. Please run again.
)

pause
