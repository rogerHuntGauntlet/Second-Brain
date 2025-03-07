@echo off
echo ===================================
echo Upload Writings to Pinecone Database
echo ===================================

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check if virtual environment exists, create if not
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% neq 0 (
        echo Failed to create virtual environment.
        exit /b 1
    )
)

REM Activate virtual environment
call .venv\Scripts\activate

REM Install requirements if needed
if not exist .venv\Lib\site-packages\openai (
    echo Installing requirements...
    pip install -r requirements_pinecone.txt
    if %ERRORLEVEL% neq 0 (
        echo Failed to install requirements.
        exit /b 1
    )
)

REM Get directory from user if not provided
set DIRECTORY=%1
if "%DIRECTORY%"=="" (
    set /p DIRECTORY="Enter directory path containing writings: "
)

REM Get namespace from user if not provided
set NAMESPACE=%2
if "%NAMESPACE%"=="" (
    set /p NAMESPACE="Enter Pinecone namespace (default: writings): "
    if "%NAMESPACE%"=="" set NAMESPACE=writings
)

REM Get file pattern from user if not provided
set PATTERN=%3
if "%PATTERN%"=="" (
    set /p PATTERN="Enter file pattern (default: **/*.md): "
    if "%PATTERN%"=="" set PATTERN=**/*.md
)

echo.
echo Running script with the following parameters:
echo Directory: %DIRECTORY%
echo Namespace: %NAMESPACE%
echo Pattern: %PATTERN%
echo.

REM Run the script
python upload_writings_to_pinecone.py --directory "%DIRECTORY%" --namespace "%NAMESPACE%" --pattern "%PATTERN%"

REM Deactivate virtual environment
call .venv\Scripts\deactivate

echo.
echo Script execution completed.
pause 