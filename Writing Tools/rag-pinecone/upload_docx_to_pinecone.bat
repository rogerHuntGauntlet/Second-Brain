@echo off
echo ===================================
echo DOCX to Pinecone Uploader
echo ===================================
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo Error creating virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Install required packages if not already installed
echo Checking required packages...
pip install -r requirements_pinecone.txt

REM Run the script
echo.
echo Starting uploader...
echo.
python docx_to_pinecone_cli.py

REM Deactivate virtual environment
call .venv\Scripts\deactivate.bat

echo.
pause 