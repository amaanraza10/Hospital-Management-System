@echo off
echo 🏥 Hospital Management System - Flask + Tkinter
echo ================================================
echo.
echo Starting system...
echo.

REM Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Start the hospital system
python run_hospital_system.py

pause