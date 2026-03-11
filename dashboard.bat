@echo off
REM Start AI Agent Dashboard Server
REM Usage: dashboard.bat

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║                                                      ║
echo ║     Starting AI Agent Dashboard Server              ║
echo ║                                                      ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found
    echo Run setup.ps1 first to create it
    echo.
)

REM Check if Flask is installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Flask not found. Installing dashboard dependencies...
    pip install flask flask-cors
)

REM Start the dashboard server
cd agent_core
python dashboard_server.py

