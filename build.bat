@echo off

REM Check for Python 3.12.5
python --version | findstr /r "Python 3\.12\.[5-9]"
if errorlevel 1 (
    echo Python 3.12.5 or higher is required.
    pause
    exit /b
)

REM Install required packages
echo Installing required Python packages...
pip install -r requirements.txt || (
    echo Failed to install required packages.
    pause
    exit /b
)


REM Check if build.py exists
if not exist "builder.py" (
    echo builder.py not found. Ensure builder.py is in the current directory.
    pause
    exit /b
)

REM Run the build Python script
echo Running the builder Python script...
python builder.py

echo Build completed.
pause