@echo off
REM Change directory to the script location
cd /d %~dp0

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies from requirements.txt (if available)
pip install -r requirements.txt

REM Alternatively, install numpy specifically if you don't have a requirements file
REM pip install numpy

REM Run the Python script
python main.py

pause
