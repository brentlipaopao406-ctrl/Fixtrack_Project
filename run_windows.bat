@echo off
setlocal
if not exist venv\Scripts\python.exe (
    echo Creating virtual environment...
    py -m venv venv
)
echo Installing/updating dependencies...
venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo Applying migrations...
venv\Scripts\python.exe manage.py migrate
if errorlevel 1 goto :error

echo.
echo Starting FixTrack at http://127.0.0.1:8000/
venv\Scripts\python.exe manage.py runserver
exit /b 0
:error
echo.
echo Setup failed. Read START_HERE.txt for manual steps.
pause
exit /b 1
