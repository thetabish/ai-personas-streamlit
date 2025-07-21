@echo off
echo 🚀 Starting AI Persona Chat Interview GUI...
echo.

REM Change to the app directory
cd /d "c:\Users\tabis\OneDrive\Documents\Test\ai-personas"

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found
    call .venv\Scripts\activate.bat
) else (
    echo ❌ Virtual environment not found! Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Check if Streamlit is installed
.venv\Scripts\python.exe -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ❌ Streamlit not installed! Installing dependencies...
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

REM Start the Streamlit app
echo.
echo 🎉 Starting Streamlit GUI...
echo 💡 The app will open in your default browser
echo 🛑 Press Ctrl+C to stop the app
echo.

.venv\Scripts\streamlit.exe run gui_app.py

pause
