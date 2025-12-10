@echo off
echo ================================
echo    Starting FinBot...
echo ================================
echo.

REM Detect project directory (folder where this BAT file is located)
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo ✔ Current directory: %CD%
echo.

REM Check if Python exists
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not added to PATH.
    echo Install from: https://www.python.org/downloads/
    pause
    exit /b
)

REM Installing dependencies (only installs missing ones)
echo ✔ Installing required Python packages...
pip install streamlit pillow pytesseract reportlab >nul

echo.
echo ✔ Launching FinBot UI...
echo.

REM Run Streamlit app
python -m streamlit run finbot_streamlit.py

echo.
echo If the browser didn't open automatically, open this link manually:
echo     http://localhost:8501
echo.
pause
