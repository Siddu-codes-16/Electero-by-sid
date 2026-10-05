@echo off
echo ========================================
echo    Electero - Electronics Design Assistant
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Initialize database
echo Initializing database...
python init_db.py
echo.

REM Run the application
echo Starting Electero...
echo Open your browser at: http://localhost:5000
echo.
python app.py
